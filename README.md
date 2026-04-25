Django Todo List Application

A full-stack Todo List web application built with Django, MongoDB, and JavaScript. This project demonstrates a clean REST API architecture with a responsive frontend for managing tasks.

Overview

This application provides both a web interface and REST API for managing todos. Users can create, read, update, and delete tasks through the browser or API endpoints.

Local Development URL: http://127.0.0.1:8000/

Features
Full task management (create, update, delete)
REST API with complete CRUD operations
MongoDB integration using PyMongo
Clean and responsive user interface
Separation of frontend and backend logic
CSRF protection via Django
Technology Stack
Backend: Django
Language: Python 3.8+ (recommended 3.10 or 3.11)
Database: MongoDB
API: Django REST Framework
Frontend: HTML, CSS, JavaScript
Database Driver: PyMongo
Prerequisites
Python (3.8 or higher)
MongoDB (running on localhost:27017)
pip (Python package manager)
Git (optional)
Quick Start

Clone the repository and navigate into the project:

git clone
cd project

Create a virtual environment:

python -m venv venv

Activate it:

Windows: venv\Scripts\activate
macOS/Linux: source venv/bin/activate

Install dependencies:

pip install django djangorestframework pymongo

Make sure MongoDB is running locally on:

mongodb://localhost:27017/

Run the server:

python manage.py runserver

Open in browser:

http://127.0.0.1:8000/

Project Structure

project/
├── project/ (Django configuration)
├── todolist/ (main app)
│ ├── models.py (MongoDB connection)
│ ├── views.py (API logic)
│ ├── urls.py (routing)
│ ├── templates/
│ └── static/
├── manage.py
└── README.md

API Endpoints

GET /api/todos/ — Retrieve all todos
POST /api/todos/ — Create a new todo
GET /api/todos/{id}/ — Retrieve a specific todo
PUT /api/todos/{id}/ — Update a todo
DELETE /api/todos/{id}/ — Delete a todo

All endpoints return JSON responses and require trailing slashes.

Architecture

Frontend → Django API → MongoDB → Response → Frontend

Frontend: Handles UI and requests
Backend: Processes logic via Django views
Database: Stores data in MongoDB
Common Issues

MongoDB connection error
Ensure MongoDB is running

Server not starting
Check Python and installed dependencies

Static files not loading
Run: python manage.py collectstatic

Future Improvements
Authentication system
Task priorities
Due dates
Search functionality
UI improvements
License

This project is for educational purposes.

Resources

Django: https://docs.djangoproject.com/
MongoDB: https://docs.mongodb.com/
PyMongo: https://pymongo.readthedocs.io/

Summary

A simple and complete Django + MongoDB Todo application demonstrating REST API development and frontend integration.
