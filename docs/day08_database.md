# Day 8 - Database Integration (PostgreSQL) 🚀

## 📌 What I Learned

### 1. SQLAlchemy

* ORM (Object Relational Mapping) for Python
* Allows interaction with database using Python code instead of raw SQL

---

### 2. PostgreSQL

* Production-level relational database
* Supports scalability and multiple users
* Better than SQLite for real-world applications

---

### 3. Environment Variables (.env)

* Used to store sensitive data like database credentials
* Prevents exposing passwords in code

Example:
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/fastapi_db

---

### 4. Database Flow

* Create engine (DB connection)
* Create session (DB interaction)
* Define models (tables)
* Perform operations (CRUD)

---

### 5. Models vs Schemas (IMPORTANT )

* **Models (SQLAlchemy)** → Define database tables
* **Schemas (Pydantic)** → Define API request/response structure

---

### 6. Dependency Injection (get_db)

* Provides database session to routes
* Ensures connection is opened and closed properly

---

##  Example

### Create Todo

POST /todos/

{
"title": "Learn PostgreSQL with FastAPI"
}

---

## 🎯 Conclusion

Integrated FastAPI with PostgreSQL using SQLAlchemy, applied clean architecture with models and schemas, and secured credentials using environment variables.
