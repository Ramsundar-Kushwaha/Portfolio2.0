'use strict'
const counter = document.querySelector("#counter");
const project_list_length = document.querySelector("tbody").children.length
console.log(counter);
console.log(project_list_length.length);

counter.textContent = project_list_length;