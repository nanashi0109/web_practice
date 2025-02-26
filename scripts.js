const tasks_container = document.getElementById("tasks-container");

const create_task = function(header_text, desctioption_text) {
    const task = document.createElement("div");
    const header = document.createElement("h1");
    const description = document.createElement("p");

    header.innerHTML = header_text;
    description.innerHTML = desctioption_text;

    task.appendChild(header);
    task.appendChild(description);

    tasks_container.appendChild(task);
}

const task_list = [
    {"header":"Hahaha", "description": "some description"}, 
    {"header":"Title 2", "description": "desc of second task"}
]

fetch("http://127.0.0.1:8000/", {
    method: "POST",
    headers: {
        "Content-Type" : "application/json"
    },
    body: JSON.stringify({header: "a", description: "b"})
})
    .then(resoponse=> resoponse.json())
    .then(data => {
    for(let da of data)
        {
            create_task(da["header"], da["description"])
        }
})
.catch(error => console.error("Error: ", error));



fetch("http://127.0.0.1:8000/hi", {
    method: "GET",
    mode: "no-cors"
})
.then(response => console.log(response))
.catch(error => console.log(error))
