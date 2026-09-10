async function loadDishes() {
    const response = await fetch('/dishes');
    const dishes = await response.json();

    const list = document.getElementById('dishList');
    const select = document.getElementById('dishSelect');
    list.innerHTML = '';
    select.innerHTML = '';

    for (const dish of dishes) {
        const li = document.createElement('li');
        li.innerHTML = `${dish.name} (${dish.category}) <button onclick="deleteDish(${dish.id})">Удалить</button>`;
        list.appendChild(li);

        const option = document.createElement('option');
        option.value = dish.id;
        option.textContent = dish.name;
        select.appendChild(option);
    }
}

async function addDish() {
    const name = document.getElementById('dishName').value;
    const category = document.getElementById('dishCategory').value;

    const response = await fetch('/dishes', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name, category})
    });

    if (!response.ok) {
        alert('Ошибка добавления блюда');
        return;
    }

    document.getElementById('dishName').value = '';
    document.getElementById('dishCategory').value = '';
    await loadDishes();
    await loadMenu();
}

async function deleteDish(id) {
    await fetch(`/dishes/${id}`, {method: 'DELETE'});
    await loadDishes();
    await loadMenu();
}

async function addDishToMenu() {
    const menuDate = document.getElementById('menuDate').value;
    const dishId = document.getElementById('dishSelect').value;

    if (!menuDate || !dishId) {
        alert('Выберите дату и блюдо');
        return;
    }

    const response = await fetch(`/menu/${menuDate}/dishes/${dishId}`, {method: 'POST'});
    if (!response.ok) {
        const error = await response.json();
        alert(error.detail);
        return;
    }

    await loadMenu();
}

async function removeDishFromMenu(menuDate, dishId) {
    await fetch(`/menu/${menuDate}/dishes/${dishId}`, {method: 'DELETE'});
    await loadMenu();
}

async function loadMenu() {
    const response = await fetch('/menu');
    const days = await response.json();
    const container = document.getElementById('menuList');
    container.innerHTML = '';

    for (const day of days) {
        const block = document.createElement('div');
        block.className = 'day';

        const dishesHtml = day.dishes.length
            ? day.dishes.map(dish => `${dish.name} <button onclick="removeDishFromMenu('${day.date}', ${dish.id})">Убрать</button>`).join('<br>')
            : 'Меню не сформировано';

        block.innerHTML = `<strong>${day.date}</strong><br>${dishesHtml}`;
        container.appendChild(block);
    }
}

loadDishes();
loadMenu();
