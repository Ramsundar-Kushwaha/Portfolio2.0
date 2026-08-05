"use strict"

const popup = document.querySelector("#popup")

if(popup){
    setInterval(()=>{
        popup.remove();
    }, 2000);
}