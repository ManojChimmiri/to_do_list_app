document.addEventListener('DOMContentLoaded', () => {
    const newTodoForm = document.getElementById('new-todo-form');
    const newTodoInput = document.getElementById('new-todo');
    const todoList = document.getElementById('todo-list');

    newTodoForm.addEventListener('submit', (e) => {
        e.preventDefault();
        addTodoItem(newTodoInput.value);
        newTodoInput.value = '';
    });

    function addTodoItem(todoText) {
        const li = document.createElement('li');
        li.innerHTML = `
            <span>${todoText}</span>
            <button class="complete-btn">Complete</button>
            <button class="delete-btn">Delete</button>
        `;
        todoList.appendChild(li);
        attachEventListeners(li);
    }

    function attachEventListeners(li) {
        li.querySelector('.complete-btn').addEventListener('click', () => {
            li.querySelector('span').classList.toggle('completed');
        });
        li.querySelector('.delete-btn').addEventListener('click', () => {
            todoList.removeChild(li);
        });
    }
});
