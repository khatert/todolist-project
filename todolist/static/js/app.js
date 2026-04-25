const API = '/api/todos/';
let todos = [];

async function loadTodos() {
  const res  = await fetch(API);
  const json = await res.json();
  todos = json.data;
  render();
}

async function createTodo() {
  const title = document.getElementById('input-title').value.trim();
  if (!title) return alert('Title is required');
  await fetch(API, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title })
  });
  document.getElementById('input-title').value = '';
  loadTodos();
}

async function updateTodo(id) {
  const title = document.getElementById(`edit-${id}`).value.trim();
  if (!title) return alert('Title is required');
  try {
    const res = await fetch(`${API}${id}/`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title })
    });
    const json = await res.json();
    console.log('Update response:', json);
    loadTodos();
  } catch (error) {
    console.error('Update error:', error);
    alert('Failed to update');
  }
}

async function deleteTodo(id) {
  await fetch(`${API}${id}/`, { method: 'DELETE' });
  loadTodos();
}

function render() {
  document.getElementById('todo-list').innerHTML = todos.map(todo => `
    <div class="todo-item">
      <input id="edit-${todo.id}" value="${todo.title}" />
      <button class="btn-update" onclick="updateTodo('${todo.id}')">Update</button>
      <button class="btn-delete" onclick="deleteTodo('${todo.id}')">Delete</button>
    </div>
  `).join('');
}

loadTodos();