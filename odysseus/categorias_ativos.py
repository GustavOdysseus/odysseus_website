import json

categories = {
    # Forex Majors e Crosses
    "AUDCAD": {"category": "forex"},
    "AUDCHF": {"category": "forex"},
    "AUDJPY": {"category": "forex"},
    "AUDNZD": {"category": "forex"},
    "AUDUSD": {"category": "forex"},
    "CADCHF": {"category": "forex"},
    "CADJPY": {"category": "forex"},
    "CHFJPY": {"category": "forex"},
    "EURAUD": {"category": "forex"},
    "EURCAD": {"category": "forex"},
    "EURCHF": {"category": "forex"},
    "EURCZK": {"category": "forex"},
    "EURDKK": {"category": "forex"},
    "EURGBP": {"category": "forex"},
    "EURHUF": {"category": "forex"},
    "EURJPY": {"category": "forex"},
    "EURTRY": {"category": "forex"},
    "EURUSD": {"category": "forex"},
    "GBPAUD": {"category": "forex"},
    "GBPCAD": {"category": "forex"},
    "GBPCHF": {"category": "forex"},
    "GBPJPY": {"category": "forex"},
    "GBPNZD": {"category": "forex"},
    "GBPUSD": {"category": "forex"},
    "NZDCAD": {"category": "forex"},
    "NZDCHF": {"category": "forex"},
    "NZDJPY": {"category": "forex"},
    "USDHUF": {"category": "forex"},

    # Commodities
    "BCOUSD": {"category": "commodity"},  # Brent Crude Oil
    "AUXAUD": {"category": "metal"},      # Gold em AUD
    "XPTUSD": {"category": "metal"},      # Platinum

    # Índices
    "DAT": {"category": "index"},         # German DAX Index
    "ETXEUR": {"category": "index"},      # Euro STOXX 50
    "EUSTX50": {"category": "index"},     # Euro STOXX 50
    "FRXEUR": {"category": "index"},      # French CAC 40
    "GRXEUR": {"category": "index"},      # German DAX
    "HKXHKD": {"category": "index"},      # Hong Kong Hang Seng
    "JPXJPY": {"category": "index"},      # Japanese Nikkei
    "NSXUSD": {"category": "index"},      # US Nasdaq
    "UKXGBP": {"category": "index"},      # UK FTSE 100
}

# Salvar categorias em um arquivo JSON
with open("symbol_categories.json", "w") as f:
    json.dump(categories, f, indent=4)

# Para verificar a distribuição das categorias
category_count = {}
for symbol, info in categories.items():
    cat = info["category"]
    category_count[cat] = category_count.get(cat, 0) + 1

print("\nDistribuição das categorias:")
for category, count in category_count.items():
    print(f"{category}: {count} símbolos")
