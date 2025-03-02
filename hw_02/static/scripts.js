const backendUrl = 'http://localhost:8000';


const catsContainer = document.getElementById("cats-container")

const createCat = function(name, age, id, count_like){
    const cat = document.createElement("div");
    cat.classList.add("cat")

    const deleteButton = document.createElement("button")
    deleteButton.classList.add("remove-button")
    deleteButton.innerHTML = "X"

    const nameElement = document.createElement("h4");
    nameElement.classList.add("base-text");
    const ageElement = document.createElement("p");
    ageElement.classList.add("base-text");

    nameElement.innerHTML = name;
    ageElement.innerHTML = age + " лет";

    const likeContainer = document.createElement("div");
    likeContainer.classList.add("like-container");
    
    const likeButton = document.createElement("button");
    likeButton.innerHTML = "Поставить лайк";
    
    const likeCounter = document.createElement("p");
    likeCounter.innerHTML = count_like;

    likeContainer.appendChild(likeButton);
    likeContainer.appendChild(likeCounter);
    
    cat.append(deleteButton, nameElement, ageElement, likeContainer);

    deleteButton.onclick = () => {
        deleteCat(id)
        .then(() => getCats())
        .then(cats => {
            document.getElementById("cats-container").innerText = ""; 
            cats.forEach(cat => { createCat(cat.name, cat.age, cat.id, cat.count_likes)});
        })
        .catch(error => console.log(error));
    }

    likeButton.onclick = () => {
        patchLike(id)
        .then(() => getCats())
        .then(cats => {
            document.getElementById("cats-container").innerText = ""; 
            cats.forEach(cat => { createCat(cat.name, cat.age, cat.id, cat.count_likes)});
        })
        .catch(error => console.log(error));
    }

    catsContainer.appendChild(cat)
}

const deleteCat = (cat_id) => {
    return fetch(backendUrl + "/cats/" + cat_id, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .catch(error => console.log(error));
}

const postCat = function(name_cat, age_cat) {
    return fetch(backendUrl + "/cats", {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name: name_cat, age: age_cat})
    })
    .then(response => response.json())
    .catch(error => console.log(error))
}

const patchLike = function(cat_id) {
    return fetch(backendUrl + "/cats/" +  cat_id + "/like", {
        method: 'PATCH',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({cat_id: cat_id})
    })
    .then(response => response.json())
    .catch(error => console.log(error))
}


const getCats = async() => {
    try {
        const response = await fetch(backendUrl + '/cats');
        const data = await response.json();
        return data.cats || [];
    }
    catch (error){
        console.log(error);
        return [];
    }
}


window.onload = () => {
    getCats()
    .then((cats)=> {
        document.getElementById('cats-container').innerHTML = "";
        cats.forEach(cat => { createCat(cat.name, cat.age, cat.id, cat.count_likes)});
    })
    .catch(error => console.log(error));
}

document.getElementById('cat-add-button').onclick = () => {
    const name = document.getElementById("name-input").value;
    const age = document.getElementById("age-input").value;

    postCat(name, age)
    .then(() => getCats())
    .then(cats => {
        document.getElementById("cats-container").innerHTML = '';
        cats.forEach(cat => { createCat(cat.name, cat.age, cat.id, cat.count_likes)});
    })
    .catch(error => console.log(error));
}
