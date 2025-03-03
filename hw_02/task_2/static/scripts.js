const backendUrl = 'http://localhost:8000';

const container = document.getElementById("currency-container");

const createCurrency = function(name, rate) {

    

    const currency = document.createElement("div");
    currency.classList.add("currency");

    const deleteButton = document.createElement("button");
    deleteButton.classList.add("delete-button");
    deleteButton.innerHTML = "X"

    const currencyName = document.createElement("h3");
    currencyName.classList.add("name");
    currencyName.innerHTML = name

    const currencyRate = document.createElement("p");
    currencyRate.classList.add("rate");
    currencyRate.innerHTML = rate;

    deleteButton.onclick = () => {
        deleteCurrency(name)
        .then(() => getCurrenccies())
        .then(currencies => recreateContainer(currencies))
        .catch(error => console.log(error));
    };

    currency.appendChild(deleteButton);
    currency.appendChild(currencyName);
    currency.appendChild(currencyRate);

    container.appendChild(currency);
}

const getCurrenccies = async function() {
    try{
        const response = await fetch(backendUrl + "/exchange-rates");
        const data = await response.json();
        return data.currencies || [] ;
    }
    catch (error){
        console.log(error);
        return [];
    }
}

const deleteCurrency = function(currency) {
    return fetch(backendUrl + "/rate/" + currency, {
        method: "DELETE",
    })
    .then(response => response.json())
    .catch(error => console.log(error));
}

const addCurrency = function(name, rate) {
    return fetch(backendUrl + "/convert", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name: name, rate: rate})
    })
    .then(response => response.json())
    .catch(error => console.log(error));
}

const updateRate = function(name, rate) {
    return fetch(backendUrl + "/update-rate/" + name, {
        method: 'PATCH',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name: name, rate: rate})
    })
    .then(response => response.json())
    .catch(error => console.log(error));
}

window.onload = () => {
    getCurrenccies()
    .then((currencies) => {recreateContainer(currencies); })
    .catch(error => console.log(error))
}

document.getElementById("add-currency").onclick = () => {
    c_name = document.getElementById("input-name").value;
    rate = document.getElementById("input-rate").value;

    addCurrency(c_name, rate)
    .then(() => getCurrenccies())
    .then(currencies => recreateContainer(currencies))
    .catch(error => console.log(error));
    
}

document.getElementById("update-currency").onclick = () => {
    c_name = document.getElementById("input-name").value;
    rate = document.getElementById("input-rate").value;

    updateRate(c_name, rate)
    .then(() => getCurrenccies())
    .then(currencies => recreateContainer(currencies))
    .catch(error => console.log(error));
}

const recreateContainer = function(currencies) {
    container.innerHTML = "";
    currencies.forEach(currency => createCurrency(currency.name, currency.rate))
}