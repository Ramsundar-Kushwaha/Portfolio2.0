"use strict"

const greeting = ["Namaste", "Hello", "Good Morning"];
let index = 0;

setInterval(() => {
    document.getElementById("greet").innerText = greeting[index];
    index = (index + 1) % greeting.length;
}, 2000);
