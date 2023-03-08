/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
const toggleTodoDropDown = () => {
  document.getElementById("todo-dropdown").classList.toggle("show");
}

const toggleDoingDropDown = () => {
  document.getElementById("doing-dropdown").classList.toggle("show");
}

const toggleDoneDropDown = () => {
    document.getElementById("done-dropdown").classList.toggle("show");
}

// code below was create by Web Dev Simplified and slightly modified to work with my project
// https://www.youtube.com/watch?v=jfYWwQrtzzY
// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.todo-dropbtn')) {
    var dropdowns = document.getElementsByClassName("todo-dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
  if (!event.target.matches('.doing-dropbtn')) {
    var dropdowns = document.getElementsByClassName("doing-dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
  if (!event.target.matches('.done-dropbtn')) {
    var dropdowns = document.getElementsByClassName("done-dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}
