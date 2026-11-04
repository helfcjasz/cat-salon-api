let items = [];


const tbody = document.querySelector('#visit-body');
const form = document.querySelector('#visit-form');
const message = document.querySelector('#message');

console.log(tbody, form, message);


function renderTable() {
  tbody.innerHTML = '';

  items.forEach(function (item) {
    const row = document.createElement('tr');

    const nameCell = document.createElement('td');
    nameCell.textContent = item.catName;

    const breedCell = document.createElement('td');
    breedCell.textContent = item.catBreed;

    const serviceTypeCell = document.createElement('td');
    serviceTypeCell.textContent = item.serviceType;

    const serviceDateCell = document.createElement('td');
    serviceDateCell.textContent = item.serviceDate;

    const catMassCell = document.createElement('td');
    catMassCell.textContent = item.catMass;

    const confirmationCell = document.createElement('td');
    confirmationCell.textContent = item.confirmation ? 'так' : 'ні';

    const actionCell = document.createElement('td');
    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Видалити';
    deleteButton.className = 'btn-delete';
    deleteButton.dataset.id = item.id;
    actionCell.append(deleteButton);


    row.append(nameCell, breedCell, serviceTypeCell, serviceDateCell, catMassCell, confirmationCell, actionCell);
    tbody.append(row);
  });
}

renderTable();




form.addEventListener('submit', async function (event) {
    event.preventDefault();

    const catName = document.querySelector('#name').value;
    const catBreed = document.querySelector('#breed').value;
    const serviceType = document.querySelector('#service').value;
    const serviceDate = document.querySelector('#visit').value;
    const catMass = Number(document.querySelector('#weight').value);
    const confirmation = document.querySelector('#confirmed').checked;

    message.textContent = '';

    if (catName === '') {
        message.textContent = 'Вкажіть кличку котика';
        return;
    }

    if (catMass < 1 || catMass > 20) {
        message.textContent = 'Маса кота не входить в адекватний діапазон';
        return;
    }

    if (serviceDate === '') {
        message.textContent = 'Вкажіть дату запису';
        return;
    }




    const newItem = {
        catName: catName,
        catBreed: catBreed,
        serviceType: serviceType,
        serviceDate: serviceDate,
        catMass: catMass,
        confirmation: confirmation
    };

    try {
      const response = await fetch('/api/items', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newItem)
      });

      if (!response.ok) {
        const error = await response.json();
        message.textContent = error.error;
        return;
      }

      const created = await response.json();
      items.push(created);
      renderTable();
      form.reset();
      message.textContent = 'Запис додано';
    } catch (error) {
      message.textContent = 'Сервер недоступний';
    }

    form.reset();
    message.textContent = 'Запис додано';

});



tbody.addEventListener('click', async function (event) {
  const id = event.target.dataset.id;
  if (!id) {
    return;
  }

  try {
    const response = await fetch('/api/items/' + id, { method: 'DELETE' });

    if (!response.ok) {
      message.textContent = 'Не вдалося видалити запис';
      return;
    }

    items = items.filter(item => item.id !== Number(id));
    renderTable();
    message.textContent = 'Запис видалено';
  } catch (error) {
    message.textContent = 'Сервер недоступний';
  }
});










async function loadItems() {
  try {
    const response = await fetch('/api/items');
    items = await response.json();
    renderTable();
  } catch (error) {
    message.textContent = 'Сервер недоступний';
  }
}


loadItems();