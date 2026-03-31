"use strict"
const owner = "<Ramsundar/>";
let textLength = owner.length;
const loading = document.querySelector("#loading");
console.log(loading);

let index = 0;
function typeWritter(){
    if(index < textLength){
        loading.textContent += owner.charAt(index);
        index++;
        setTimeout(typeWritter, 100);
    }
}

typeWritter();