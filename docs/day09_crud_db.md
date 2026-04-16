# Day 9 - CRUD Operations with Database 🚀

## 📌 What I Learned

### 1. CRUD Operations

* Create → Add new data
* Read → Fetch data
* Update → Modify existing data
* Delete → Remove data

---

### 2. Database Integration

* Used PostgreSQL database
* Connected using SQLAlchemy
* Data is now stored permanently

---

### 3. API Endpoints

#### ➤ Create Todo

POST /todos/

Input:
{
"title": "Learn FastAPI"
}

---

#### ➤ Get All Todos

GET /todos/

---

#### ➤ Get Single Todo

GET /todos/{id}

---

#### ➤ Update Todo

PUT /todos/{id}

Input:
{
"title": "Master FastAPI",
"completed": true
}

---

#### ➤ Delete Todo

DELETE /todos/{id}

---

### 4. Error Handling

* Used HTTPException
* Returned 404 if todo not found

---

### 5. Schema Usage

* TodoCreate → for creating data
* TodoUpdate → for updating data
* TodoResponse → for API response

---

##  Example Flow

1. Create Todo
2. Get Todos
3. Update Todo (mark completed = true)
4. Delete Todo

---

## 🎯 Conclusion

Implemented full CRUD operations using FastAPI with PostgreSQL database and followed clean structure using models and schemas.
