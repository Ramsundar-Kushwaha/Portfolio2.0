'use strict'
// ----- for showing number of project in list -----
const counter = document.querySelector("#counter");
const project_list_length = document.querySelector("main").children.length

console.log(counter);
console.log(project_list_length.length);

counter.textContent = project_list_length;