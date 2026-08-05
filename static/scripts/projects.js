"use strict"

const project_list = document.querySelector("main")
const project_list_heading = document.querySelector("h3");
const project_list_length = project_list.children.length;

if(project_list_length == 0){
    project_list_heading.textContent = "Empty List";
}else{
    project_list_heading.textContent = "Project List";
}
