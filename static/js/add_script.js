const title_label = document.getElementById("title-label");
const description_label = document.getElementById("description-label");
const due_date_label = document.getElementById("due-date-label");
const cancel_btn = document.getElementById("cancel-btn");

const show_title_input = () => {
    const title_input = document.getElementById("title-input");
    title_input.classList.toggle("show");
}

const show_description_input = () => {
    const description_input = document.getElementById("description-input");
    description_input.classList.toggle("show");
}

const show_due_date_input = () => {
    const due_date_input = document.getElementById("due-date-input");
    due_date_input.classList.toggle("show");
}

const cancel = (event) => {
    event.target.setAttribute("value", "True");
}

title_label.addEventListener('click', show_title_input);
description_label.addEventListener('click', show_description_input);
due_date_label.addEventListener('click', show_due_date_input);
cancel_btn.addEventListener('click', cancel);