const draggables = document.querySelectorAll('.draggable')
const containers = document.querySelectorAll('.container')

let start_container;

const update_db = async (data, end_container, start_container) => {
    let title;
    let description;
    let due_date;

    try{
        title = data.children[0].children[0].innerHTML;
    } catch(error) {
        title = "None"
    }
    try {
        description = data.children[1].innerHTML
    } catch (error) {
        description = "None";
    }
    try{
        due_date = data.children[2].children[0].innerHTML
    } catch(error) {
        due_date = "None";
    }

    let json_data = {
        "title": title,
        "description": description,
        "due_date": due_date,
        "end_container": end_container,
        "start_container": start_container,
    }

    const response = await fetch("../../update", {
        method: "POST",
        headers: {
        "Content-Type": "application/json",
        },
        body: JSON.stringify(json_data),
    })

}

draggables.forEach(draggable => {
  draggable.addEventListener('dragstart', (event) => {
    draggable.classList.add('dragging');
    for(i=0; i < event.target.parentElement.classList.length; ++i) {
        if (event.target.parentElement.classList[i] == "todo" ||
            event.target.parentElement.classList[i] == "doing" ||
            event.target.parentElement.classList[i] == "done"){
            start_container = event.target.parentElement.classList[i]
            }
        }
  })

  draggable.addEventListener('dragend', (event) => {
    draggable.classList.remove('dragging');
    let data = event.target;
    let container;
    for(i=0; i < event.target.parentElement.classList.length; ++i) {
        if (event.target.parentElement.classList[i] == "todo" ||
            event.target.parentElement.classList[i] == "doing" ||
            event.target.parentElement.classList[i] == "done"){
            end_container = event.target.parentElement.classList[i]
            }
    }
    update_db(data, end_container, start_container)
  })
})

containers.forEach(container => {
  container.addEventListener('dragover', e => {
    e.preventDefault()
    const afterElement = getDragAfterElement(container, e.clientY)
    const draggable = document.querySelector('.dragging')
    if (afterElement == null) {
      container.appendChild(draggable)
    } else {
      container.insertBefore(draggable, afterElement)
    }
  })
})

function getDragAfterElement(container, y) {
  const draggableElements = [...container.querySelectorAll('.draggable:not(.dragging)')]

  return draggableElements.reduce((closest, child) => {
    const box = child.getBoundingClientRect()
    const offset = y - box.top - box.height / 2
    if (offset < 0 && offset > closest.offset) {
      return { offset: offset, element: child }
    } else {
      return closest
    }
  }, { offset: Number.NEGATIVE_INFINITY }).element
}