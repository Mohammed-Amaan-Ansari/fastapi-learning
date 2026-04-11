# Day 4 - Response Models 🚀

## 📌 What I Learned

### 1. response_model
- Controls API output
- Filters unwanted data

### 2. Security
- Prevents sending sensitive data like passwords

### 3. Clean API Design
- Separate request and response models

##  Example
POST /users/

Input:
{
  "name": "Amaan",
  "email": "amaan@gmail.com",
  "password": "123"
}

Output:
{
  "name": "Amaan",
  "email": "amaan@gmail.com"
}