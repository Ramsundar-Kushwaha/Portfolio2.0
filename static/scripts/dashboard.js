'use strict'

function confirmProject(){
    return confirm("Are You Sure?")

}

// for popup message
const popup = document.getElementById("popup");

if (popup) {
    setTimeout(()=>{
        popup.remove();
    }, 1500);
}


// for calendar
document.addEventListener('DOMContentLoaded', function () {

    const calendarElement = document.getElementById('calendar');

    const calendar = new FullCalendar.Calendar(calendarElement, {
        initialView: 'dayGridMonth'
    });

    calendar.render();

});

