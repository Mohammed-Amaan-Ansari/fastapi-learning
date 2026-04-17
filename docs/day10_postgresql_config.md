# Day 10 - PostgreSQL Configuration & Project Cleanup 🚀

## 📌 What I Learned

### 1. PostgreSQL Integration

* Switched from SQLite to PostgreSQL
* Used a production-level database
* Data is stored securely and supports multiple users

---

### 2. Environment Variables (.env)

* Stored database credentials in `.env` file
* Avoided exposing sensitive data in code

Example:
DATABASE_URL=postgresql://username:password@localhost:5432/fastapi_db

---

### 3. Secure Project Setup

* Added `.env` to `.git
