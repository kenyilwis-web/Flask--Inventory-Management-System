document.addEventListener('DOMContentLoaded', () => {
    const inventoryTable = document.getElementById('inventory-table').querySelector('tbody');
    const addItemForm = document.getElementById('add-item-form');
    const searchForm = document.getElementById('search-form');
    const searchResults = document.getElementById('search-results');

    // Fetch and display inventory items
    async function fetchInventory() {
        const response = await fetch('/inventory');
        const data = await response.json();

        inventoryTable.innerHTML = '';
        data.data.items.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${item.id}</td>
                <td>${item.name}</td>
                <td>${item.category}</td>
                <td>
                    <button onclick="deleteItem('${item.id}')">Delete</button>
                </td>
            `;
            inventoryTable.appendChild(row);
        });
    }

    // Add new inventory item
    addItemForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const name = document.getElementById('item-name').value;
        const category = document.getElementById('item-category').value;

        await fetch('/inventory', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, category })
        });

        addItemForm.reset();
        fetchInventory();
    });

    // Delete inventory item
    async function deleteItem(id) {
        await fetch(`/inventory/${id}`, { method: 'DELETE' });
        fetchInventory();
    }

    // Search OpenFoodFacts
    searchForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const query = document.getElementById('search-query').value;
        const response = await fetch(`/search?query=${query}`);
        const data = await response.json();

        searchResults.innerHTML = '';
        data.data.forEach(product => {
            const li = document.createElement('li');
            li.textContent = `${product.product_name} (${product.brands})`;
            searchResults.appendChild(li);
        });
    });

    // Initial fetch
    fetchInventory();
});