document.addEventListener("DOMContentLoaded", function () {
    // Configurações do mini-carrinho - fácil de ajustar depois
    const config = {
        miniCartSelectors: [
            '.mini-cart',           // Seletor comum
            '#cart-dropdown',       // Seletor comum
            '.cart-count-bubble',   // Shopify comum
            '.cart-drawer'          // Outro seletor comum
        ],
        priceSelectors: [
            '.cart-total',
            '.cart-subtotal',
            '.mini-cart-total'
        ],
        itemPriceSelectors: [
            '.cart-item-price',
            '.mini-cart-item-price'
        ]
    };

    // Função para atualizar a quantidade de um item no carrinho
    async function updateCartItemQuantity(lineId, quantity) {
        try {
            const response = await fetch('/cart/change.js', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    line: lineId,
                    quantity: quantity
                })
            });
            return await response.json();
        } catch (error) {
            console.error('Erro ao atualizar carrinho:', error);
        }
    }

    // Função para formatar preço
    function formatPrice(price) {
        return (price/100).toLocaleString('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        });
    }

    // Função para atualizar preços no mini-carrinho
    function updateMiniCartPrices(cart) {
        try {
            let totalPrice = 0;
            let hasDiscount = cart.items.length >= 2;
            
            // Encontrar item com menor preço se houver desconto
            let lowestPriceItem = hasDiscount ? cart.items.reduce((prev, current) => 
                (prev.price < current.price) ? prev : current
            ) : null;

            // Calcular total com desconto
            cart.items.forEach(item => {
                if (hasDiscount && item.id === lowestPriceItem.id) {
                    totalPrice += (item.price * item.quantity) / 2;
                } else {
                    totalPrice += item.price * item.quantity;
                }
            });

            // Atualizar preços no mini-carrinho
            config.priceSelectors.forEach(selector => {
                const elements = document.querySelectorAll(selector);
                elements.forEach(element => {
                    element.textContent = formatPrice(totalPrice);
                });
            });

            // Atualizar preços individuais dos itens
            cart.items.forEach(item => {
                const itemPrice = hasDiscount && item.id === lowestPriceItem.id
                    ? item.price / 2
                    : item.price;
                
                config.itemPriceSelectors.forEach(selector => {
                    const itemElement = document.querySelector(`${selector}[data-id="${item.id}"]`);
                    if (itemElement) {
                        itemElement.textContent = formatPrice(itemPrice);
                        if (hasDiscount && item.id === lowestPriceItem.id) {
                            itemElement.innerHTML += ' <span class="discount-badge">-50%</span>';
                        }
                    }
                });
            });
        } catch (error) {
            console.error('Erro ao atualizar mini-carrinho:', error);
        }
    }

    // Função para aplicar o desconto no carrinho
    async function applyDiscount() {
        try {
            const response = await fetch('/cart.js');
            const cart = await response.json();
            
            if (cart.items.length >= 2) {
                // Encontrar o item com menor preço para aplicar o desconto
                let lowestPriceItem = cart.items.reduce((prev, current) => 
                    (prev.price < current.price) ? prev : current
                );
                
                // Aplicar propriedade de desconto ao item
                await fetch('/cart/update.js', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        updates: {
                            [lowestPriceItem.id]: {
                                price: lowestPriceItem.price / 2,
                                properties: {
                                    '_discounted': true,
                                    '_original_price': lowestPriceItem.price
                                }
                            }
                        }
                    })
                });

                // Atualizar mini-carrinho imediatamente
                updateMiniCartPrices(cart);
            }
        } catch (error) {
            console.error('Erro ao aplicar desconto:', error);
        }
    }

    // Função para remover todos os descontos
    async function removeAllDiscounts() {
        try {
            const response = await fetch('/cart.js');
            const cart = await response.json();
            
            for (let item of cart.items) {
                if (item.properties && item.properties._discounted) {
                    await updateCartItemQuantity(item.line, item.quantity, {
                        properties: {
                            '_discounted': null,
                            '_original_price': null
                        }
                    });
                }
            }
            
            // Atualizar mini-carrinho imediatamente
            updateMiniCartPrices(cart);
        } catch (error) {
            console.error('Erro ao remover descontos:', error);
        }
    }

    // Função principal para verificar e atualizar o carrinho
    async function checkCartItems() {
        try {
            const response = await fetch('/cart.js');
            const cart = await response.json();

            // Atualizar mini-carrinho primeiro
            updateMiniCartPrices(cart);

            if (cart.items.length >= 2) {
                await applyDiscount();
            } else {
                await removeAllDiscounts();
            }
        } catch (error) {
            console.error('Erro ao verificar itens do carrinho:', error);
        }
    }

    // Adicionar CSS para o badge de desconto
    const style = document.createElement('style');
    style.textContent = `
        .discount-badge {
            background-color: #ff0000;
            color: white;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.8em;
            margin-left: 5px;
        }
    `;
    document.head.appendChild(style);

    // Monitorar mudanças no carrinho
    document.body.addEventListener("click", function (event) {
        if (event.target.matches(".cart__remove") || event.target.closest(".cart__remove")) {
            setTimeout(checkCartItems, 500);
        }
    });

    // Verificar carrinho quando a página carrega
    checkCartItems();

    // Monitorar adições ao carrinho
    document.body.addEventListener("click", function (event) {
        if (event.target.matches(".add-to-cart") || event.target.closest(".add-to-cart")) {
            setTimeout(checkCartItems, 500);
        }
    });

    // Observar mudanças no DOM para atualizar o mini-carrinho
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList' || mutation.type === 'subtree') {
                const miniCartUpdated = config.miniCartSelectors.some(selector => 
                    mutation.target.matches(selector) || 
                    mutation.target.querySelector(selector)
                );
                
                if (miniCartUpdated) {
                    checkCartItems();
                }
            }
        });
    });

    // Observar todo o documento para mudanças no mini-carrinho
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});