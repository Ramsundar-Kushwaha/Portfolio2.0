'use strict'

function confirmProject(){
    return confirm("Are You Sure You Want To Add This Project?")
}

const popup = document.getElementById("popup");
console.log(popup);

if(popup){
    setTimeout(()=>{
        popup.remove();
    }, 1500);
}
