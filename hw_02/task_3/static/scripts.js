const backendURL = "http://localhost:8000";

const parcelsContainer = document.getElementById("parcels-container");

const createParcel = function(id, name, status, weight, senders_address, destination) {
    const parcel = document.createElement("div");
    parcel.classList.add("parcel-card");

    const parcelHeader = document.createElement("h3");
    parcelHeader.classList.add("parcel-card-header");
    parcelHeader.innerHTML = id;

    const parcelName = document.createElement("p");
    parcelName.innerHTML = name;
    
    const parcelStatus = document.createElement("p");
    parcelStatus.innerHTML = status;

    const parcelWeight = document.createElement("p");
    parcelWeight.innerHTML = weight;

    const parcelAddress = document.createElement("p");
    parcelAddress.innerHTML = "from" + senders_address;

    const parcelDestination = document.createElement("p");
    parcelDestination.innerHTML = "to" + destination;

    parcel.appendChild(parcelHeader, parcelName,  parcelStatus, parcelWeight, parcelAddress, parcelDestination);

    parcelsContainer.appendChild(parcel);
}

const getAllParcels = async function(status, destination) {
    try{
        const response = await fetch(backendURL + "/parcels?status=" + status + "&destination=" + destination)
        const data = await response.json()

        return data || []; 
    }
    catch(error){
        console.log(error);
        return [];
    }
}

const addParcel = function(name, weight, senders_address, destination){
    return fetch(backendURL + "/parcels", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name: name, weight: weight, senders_address: senders_address, destination: destination})
    })
    .then(response => response.json())
    .catch(error => console.log(error));
}

const updateStatus = function(id_parcel, new_status) {
    return fetch(backendURL + "/parcel/" + id_parcel, {
        method: "PATCH",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({id: id_parcel, status: new_status})
    })
    .then(response => response.json())
    .catch(error => console.log(error));
}

const deleteParce = function(id_parcel) {
    return fetch(backendURL + "/parcels/" + id_parcel, {
        method: "DELETE",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({id: id_parcel})
    })
    .then(response => response.json())
    .catch(error => console.log(error));
}


document.getElementById("add-button").onclick = () => {
    name = document.getElementById("input-name").value;
    weight = document.getElementById("input-weight").value;
    senders_address = document.getElementById("input-senders-address").value;
    destination = document.getElementById("input-destination").value;
    
    addParcel(name, weight, senders_address, destination)
    .then(() => getAllParcels("None", "None"))
    .then(parcels => recrateParcelContainer(parcels))
    .catch(error => console.log(error));
}


const clearInputField = function() {
    document.getElementById("input-name").value = "";
    document.getElementById("input-weight").value = "";
    document.getElementById("input-senders-address").value = "";
    document.getElementById("input-destination").value = "";
}

const recrateParcelContainer = function(parcels) {
    parcelsContainer.innerHTML = "";
    
    parcels.forEach(parcel => createParcel(parcel.id, parcel.name, parcel.status, parcel.weight, parcel.senders_address, parcel.destination));
}

document.getElementById("clear-button").onclick = clearInputField;

window.onload = () => {
    getAllParcels("None", "None")
    .then(parcels => recrateParcelContainer(parcels))
    .catch(error => console.log(error));
}
