# Masterblog API

Masterblog API is a RESTful API built using **Flask**, supporting CRUD operations for managing blog posts. It also includes **search, sorting**, and **Swagger documentation**.

This is a project created as part of the Masterschool curriculum.


## 🚀 Features
- 📝 **Create, Read, Update, Delete (CRUD)** blog posts
- 🔍 **Search posts** by title or content
- 📌 **Sorting** posts by title or content (asc/desc)
- 📑 **Interactive API Documentation** with Swagger UI

---

![Alt Text](assets/screenshot.png)

---

## 🛠 Installation

### **1. Clone the Repository**
```sh
git clone https://github.com/yourusername/Masterblog-API.git
cd Masterblog-API
```

### **2. Create a Virtual Environment (Optional)**
```sh
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### **3. Install Dependencies**
```sh
pip install -r requirements.txt
```

---

## 🚦 Running the API
### **Start the Flask Server**
```sh
python backend/backend_app.py
```
The API will be available at:  
👉 `http://127.0.0.1:5002`

---

## 📖 API Documentation
### **Swagger UI**
Swagger UI is available at:  
👉 `http://127.0.0.1:5002/api/docs`

---

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|---------|-------------|
| **GET** | `/api/posts` | Get all blog posts (supports sorting) |
| **POST** | `/api/posts` | Create a new blog post |
| **GET** | `/api/posts/{id}` | Retrieve a single post by ID |
| **PUT** | `/api/posts/{id}` | Update a blog post by ID |
| **DELETE** | `/api/posts/{id}` | Delete a blog post by ID |
| **GET** | `/api/posts/search?title=flask&content=api` | Search posts by title or content |

---

## 🔧 Configuration
### **Updating the Swagger Definition**
The Swagger API documentation is stored in:  
📂 `backend/static/masterblog.json`  
Modify this file to update the documentation.

---

## 🛠 Built With
- **Flask** - Python Web Framework
- **Flask-CORS** - Handles Cross-Origin Resource Sharing
- **Flask-Swagger-UI** - Provides API documentation
- **JSON** - Stores API documentation structure

---

## 🙏 Acknowledgments

Special thanks to Masterschool for providing the guidance and resources for this project.

---
