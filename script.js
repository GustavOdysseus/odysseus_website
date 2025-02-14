document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("logs-container");
  
  fetch('https://raw.githubusercontent.com/GustavOdysseus/odysseus_website/main/transaction_logs.json')
    .then(response => {
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      return response.json();
    })
    .then(data => {
      if (!Array.isArray(data)) throw new Error('Invalid data format');
      
      container.innerHTML = '';
      if (data.length === 0) {
        container.textContent = "No transactions found.";
        return;
      }

      const list = document.createElement("ul");
      data.forEach(log => {
        const listItem = document.createElement("li");
        const content = document.createElement("div");
        
        content.innerHTML = `
          <strong>Conversation ID:</strong> <span class="log-value">${escapeHtml(log.conversation_id)}</span><br/>
          <strong>Transaction Hash:</strong> <span class="log-value">${escapeHtml(log.tx_hash)}</span><br/>
          <strong>Timestamp:</strong> <span class="log-value">${escapeHtml(new Date(log.timestamp).toLocaleString())}</span>
        `;
        
        listItem.appendChild(content);
        list.appendChild(listItem);
      });
      container.appendChild(list);
    })
    .catch(error => {
      console.error('Error:', error);
      container.textContent = `Error loading logs: ${error.message}`;
    });

  document.title = "Final Considerations | Transaction Registry";

  function escapeHtml(unsafe) {
    return unsafe?.toString()?.replace(/[&<"'>]/g, match => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;'
    }[match])) || '';
  }
});
