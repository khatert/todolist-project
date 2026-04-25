# Django Todo List Website - Complete Guide for Beginners

This guide teaches you how to build a complete Todo List website from scratch using Django and MongoDB.

---

## 📋 Table of Contents

1. [What You'll Build](#what-youll-build)
2. [Prerequisites](#prerequisites)
3. [Step-by-Step Setup](#step-by-step-setup)
4. [Project Structure](#project-structure)
5. [File Explanations](#file-explanations)
6. [API Endpoints](#api-endpoints)
7. [Running the Project](#running-the-project)
8. [Testing with Postman](#testing-with-postman)

---

## 🎯 What You'll Build

A **Todo List Website** with:
- ✅ Web interface to add/edit/delete todos
- ✅ REST API for CRUD operations
- ✅ MongoDB database integration
- ✅ Separated HTML, CSS, and JavaScript files
- ✅ Full backend with Django

### Final Result
- **Home Page:** `http://127.0.0.1:8000/` - Beautiful UI to manage todos
- **API:** `http://127.0.0.1:8000/api/todos/` - RESTful endpoints for data

---

## 📦 Prerequisites

Before starting, install:

### 1. Python
Download and install from [python.org](https://www.python.org/)
- Windows: Download installer and run it
- Check version: `python --version`

### 2. Django
```bash
pip install django
```

### 3. PyMongo (MongoDB driver for Python)
```bash
pip install pymongo
```

### 4. Django REST Framework
```bash
pip install djangorestframework
```

### 5. MongoDB
Install from [mongodb.com](https://www.mongodb.com/try/download/community)
- Make sure MongoDB is running on `localhost:27017`

### 6. MongoDB Compass (Optional)
Download from [mongodb.com/compass](https://www.mongodb.com/products/compass)
- Visual tool to view your database

---

## 🚀 Step-by-Step Setup

### Step 1: Create Django Project

```bash
django-admin startproject project
cd project
```

This creates:
```
project/
├── project/
│   ├── settings.py
│   ├── urls.py
│   └── ...
└── manage.py
```

### Step 2: Create Django App

```bash
python manage.py startapp todolist
```

This creates:
```
todolist/
├── models.py
├── views.py
├── urls.py
├── templates/
├── static/
└── ...
```

### Step 3: Configure Django Settings

Edit `project/settings.py`:

```python
# Add this line (after INSTALLED_APPS definition)
INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'rest_framework',
    'todolist',  # Add this
]

# Add at the bottom:
MONGODB_URI = 'mongodb://localhost:27017/'
MONGODB_DB = 'todolist'
```

### Step 4: Create Folder Structure

Create folders in `todolist/`:

```
todolist/
├── templates/
│   └── todos/
│       └── home.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── models.py
├── views.py
├── urls.py
└── ...
```

### Step 5: Create Models (Database Connection)

Create `todolist/models.py`:

```python
import pymongo
from django.conf import settings

_client = None
_db = None

def get_db():
    """Return a cached MongoDB database instance."""
    global _client, _db
    if _db is None:
        _client = pymongo.MongoClient(settings.MONGODB_URI)
        _db = _client[settings.MONGODB_DB]
    return _db

def get_collection(name: str):
    return get_db()[name]
```

This connects to MongoDB without using Django ORM.

### Step 6: Create Views (API Endpoints)

Create `todolist/views.py`:

```python
import json
from bson import ObjectId
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import get_collection


def index(request):
    """Render the home page."""
    return render(request, 'todos/home.html')


@csrf_exempt
def todos(request):
    """Handle GET (list all) and POST (create new)."""
    col = get_collection('todos')

    if request.method == 'GET':
        # Get all todos from MongoDB
        docs = list(col.find())
        for d in docs:
            d['id'] = str(d['_id'])
            del d['_id']
        return JsonResponse({'data': docs})

    if request.method == 'POST':
        # Create new todo
        body = json.loads(request.body)
        doc = {
            'title': body.get('title'),
            'completed': False,
        }
        result = col.insert_one(doc)
        doc['id'] = str(result.inserted_id)
        del doc['_id']
        return JsonResponse({'data': doc})


@csrf_exempt
def todo_detail(request, todo_id):
    """Handle GET (read one), PUT (update), DELETE (delete)."""
    col = get_collection('todos')
    oid = ObjectId(todo_id)

    if request.method == 'PUT':
        # Update todo
        body = json.loads(request.body)
        col.update_one({'_id': oid}, {'$set': {'title': body.get('title')}})
        doc = col.find_one({'_id': oid})
        doc['id'] = str(doc['_id'])
        del doc['_id']
        return JsonResponse({'data': doc})

    if request.method == 'DELETE':
        # Delete todo
        col.delete_one({'_id': oid})
        return JsonResponse({'message': 'Deleted'})
```

**What this does:**
- `index()` - Returns HTML home page
- `todos()` - Handles GET all, POST create
- `todo_detail()` - Handles PUT update, DELETE delete

### Step 7: Create URL Routes

Create `todolist/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/todos/', views.todos),
    path('api/todos/<todo_id>/', views.todo_detail),
]
```

Then update `project/urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    path('', include('todolist.urls')),
]
```

### Step 8: Create HTML Template

Create `todolist/templates/todos/home.html`:

```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>Todo List</title>
  <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
<div class="container">

  <h1>Todo List</h1>

  <!-- ADD -->
  <div class="add-section">
    <input type="text" id="input-title" placeholder="Add a new task..." />
    <button class="btn-add" onclick="createTodo()">Add</button>
  </div>

  <!-- LIST -->
  <div id="todo-list"></div>

</div>

<script src="{% static 'js/app.js' %}"></script>
</body>
</html>
```

### Step 9: Create CSS

Create `todolist/static/css/style.css`:

```css
* { 
  box-sizing: border-box; 
  margin: 0; 
  padding: 0; 
}

body {
  font-family: Arial, sans-serif;
  background: #f5f5f5;
  padding: 40px 20px;
}

.container {
  max-width: 500px;
  margin: 0 auto;
}

h1 {
  font-size: 24px;
  color: #333;
  margin-bottom: 20px;
}

.add-section {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
}

input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
  width: 100%;
  outline: none;
}

input:focus {
  border-color: #888;
}

button {
  padding: 10px 16px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  white-space: nowrap;
}

.btn-add    { background: #333; color: #fff; }
.btn-update { background: #5a9e6f; color: #fff; }
.btn-delete { background: #c0392b; color: #fff; }

.todo-item {
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 12px;
  margin-bottom: 8px;
  display: flex;
  gap: 8px;
  align-items: center;
}

.todo-item input {
  border: 1px solid #eee;
  background: #fafafa;
  flex: 1;
}

.todo-item input:focus {
  border-color: #888;
  background: #fff;
}
```

### Step 10: Create JavaScript

Create `todolist/static/js/app.js`:

```javascript
const API = '/api/todos/';
let todos = [];

// Load all todos when page loads
async function loadTodos() {
  const res  = await fetch(API);
  const json = await res.json();
  todos = json.data;
  render();
}

// Create new todo
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

// Update todo
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
    loadTodos();
  } catch (error) {
    console.error('Update error:', error);
    alert('Failed to update');
  }
}

// Delete todo
async function deleteTodo(id) {
  await fetch(`${API}${id}/`, { method: 'DELETE' });
  loadTodos();
}

// Render todos on page
function render() {
  document.getElementById('todo-list').innerHTML = todos.map(todo => `
    <div class="todo-item">
      <input id="edit-${todo.id}" value="${todo.title}" />
      <button class="btn-update" onclick="updateTodo('${todo.id}')">Update</button>
      <button class="btn-delete" onclick="deleteTodo('${todo.id}')">Delete</button>
    </div>
  `).join('');
}

// Load todos when page loads
loadTodos();
```

---

## 📁 Project Structure

Final structure:

```
project/
├── project/
│   ├── settings.py          # Django config
│   ├── urls.py              # Main URL routes
│   └── ...
├── todolist/
│   ├── templates/todos/
│   │   └── home.html        # HTML template
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # Styling
│   │   └── js/
│   │       └── app.js       # JavaScript logic
│   ├── models.py            # MongoDB connection
│   ├── views.py             # API endpoints
│   ├── urls.py              # App routes
│   └── ...
├── manage.py                # Django management
└── README.md                # Documentation
```

---

## 📝 File Explanations

### `models.py` - Database Connection
- Connects to MongoDB
- `get_db()` returns database instance
- `get_collection(name)` returns a collection

### `views.py` - API Endpoints
- `index()` - Serves HTML page
- `todos()` - GET all, POST create
- `todo_detail()` - PUT update, DELETE delete

### `urls.py` - URL Routing
- Maps URLs to views
- `''` → home page
- `api/todos/` → list/create todos
- `api/todos/<id>/` → update/delete specific todo

### `home.html` - User Interface
- Input field to add todos
- Div where todos are rendered
- Links to CSS and JavaScript

### `style.css` - Styling
- Colors, fonts, spacing
- Button styles
- Responsive layout

### `app.js` - Frontend Logic
- Fetches data from API
- Handles add, update, delete
- Renders todos on page

---

## 🔌 API Endpoints

### Get All Todos
```
GET /api/todos/
Response: {"data": [{id: "...", title: "Buy milk", completed: false}, ...]}
```

### Create Todo
```
POST /api/todos/
Body: {"title": "Buy milk"}
Response: {"data": {id: "...", title: "Buy milk", completed: false}}
```

### Update Todo
```
PUT /api/todos/<id>/
Body: {"title": "Updated title"}
Response: {"data": {id: "...", title: "Updated title", completed: false}}
```

### Delete Todo
```
DELETE /api/todos/<id>/
Response: {"message": "Deleted"}
```

---

## 🏃 Running the Project

### 1. Make sure MongoDB is running
```bash
# Windows
# MongoDB should be running in background
# Or run: mongod
```

### 2. Start Django server
```bash
python manage.py runserver
```

Output:
```
Watching for file changes with StatReloader
Performing system checks...
System check identified no issues (0 silenced).
Starting development server at http://127.0.0.1:8000/
```

### 3. Open browser
Go to: **http://127.0.0.1:8000/**

You should see the Todo List app!

---

## 🧪 Testing with Postman

### 1. Download Postman
From [postman.com](https://www.postman.com/downloads/)

### 2. Create Requests

#### GET All Todos
- Method: **GET**
- URL: `http://127.0.0.1:8000/api/todos/`
- Click **Send**

#### Create Todo
- Method: **POST**
- URL: `http://127.0.0.1:8000/api/todos/`
- Body → raw → JSON:
  ```json
  {"title": "Buy groceries"}
  ```
- Click **Send**

#### Update Todo
- Copy the `id` from GET response
- Method: **PUT**
- URL: `http://127.0.0.1:8000/api/todos/{id}/`
- Body → raw → JSON:
  ```json
  {"title": "Updated title"}
  ```
- Click **Send**

#### Delete Todo
- Method: **DELETE**
- URL: `http://127.0.0.1:8000/api/todos/{id}/`
- Click **Send**

---

## 📊 How It Works (Data Flow)

```
1. User opens http://127.0.0.1:8000/
   ↓
2. Django returns home.html
   ↓
3. Browser loads app.js
   ↓
4. app.js calls fetch('/api/todos/') → GET request
   ↓
5. Django views.py handles GET request
   ↓
6. views.py queries MongoDB
   ↓
7. MongoDB returns todos
   ↓
8. views.py returns JSON to frontend
   ↓
9. app.js receives data and calls render()
   ↓
10. render() displays todos on page
   ↓
11. User clicks "Add" button
   ↓
12. createTodo() sends POST to /api/todos/
   ↓
13. Repeat: GET request updates page
```

---

## 🎓 Key Concepts

### Django
- **Framework** for building web applications
- Handles routing, templates, security
- Connects frontend to backend

### MongoDB
- **NoSQL database** (not SQL)
- Stores data as JSON documents
- No tables, no schemas

### PyMongo
- **Python driver** for MongoDB
- Lets Python code talk to MongoDB
- Handles insert, find, update, delete

### REST API
- **Requests:** GET, POST, PUT, DELETE
- **URLs:** Point to resources (todos)
- **Responses:** JSON format

### Fetch API
- **JavaScript** function to make HTTP requests
- Used in app.js to call backend
- Returns JSON data

---

## 🐛 Common Issues & Fixes

### Issue: "MongoDB connection refused"
**Fix:** Make sure MongoDB is running
```bash
mongod  # Start MongoDB
```

### Issue: "404 Not Found" on home page
**Fix:** Check `urls.py` has correct paths

### Issue: Todos don't show after adding
**Fix:** Check browser console (F12) for errors

### Issue: CSS not loading
**Fix:** Make sure `static/css/style.css` exists

---

## 🚀 Next Steps (Improvements)

You can add:
- ✅ User authentication (login/register)
- ✅ Priority levels (high, medium, low)
- ✅ Due dates for todos
- ✅ Categories/tags
- ✅ Search functionality
- ✅ Dark mode
- ✅ Mobile responsive design

---

## 📚 Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)
- [MDN Web Docs - Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)

---

## ✅ Summary

You now have a complete Todo List website with:
- ✅ Django backend with REST API
- ✅ MongoDB database
- ✅ Beautiful frontend
- ✅ Add, edit, delete todos
- ✅ Professional file structure

**Congratulations! 🎉**

