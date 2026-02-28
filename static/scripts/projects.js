"use strict"

const project_list = document.querySelector("main")
const form = document.querySelector("form");
console.log(project_list, form);

// form.addEventListener('submit', (event)=>{
//     event.preventDefault();

//     // gets value of title and description form project.html
//     const title = event.target.title.value;
//     const description = event.target.desc.value;

//     // creating html elements for insertion in the page
//     const project_card = document.createElement("div");
//     const project_title = document.createElement("div");
//     const project_description = document.createElement("div");

//     // adding respective class to the created elements
//     project_card.classList.add("project_card");
//     project_title.classList.add("project_title");
//     project_description.classList.add("project_description");

//     // updating text content in the created elements
//     project_title.textContent = title;
//     project_description.textContent = description;

//     // updating page
//     project_card.append(project_title);
//     project_card.append(project_description);
//     project_list.prepend(project_card);

//     this.reset();

// });


const project_list_heading = document.querySelector("h2");
const project_list_length = project_list.children.length;

if(project_list_length == 0){
    project_list_heading.textContent = "Empty List";
}else{
    project_list_heading.textContent = "Project List";
}
