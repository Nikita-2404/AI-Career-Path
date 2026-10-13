# 🚀 AI Career Path – Career Recommendation System

## 📌 Project Overview

AI Career Path is a web-based career recommendation system developed
to help users identify suitable career options based on their skills,
education, interests, and other relevant information.

The system uses Machine Learning to predict career options and provides
career roadmaps, job opportunities, and prediction history through
a user-friendly web interface.

## 🎯 Project Objectives

- Recommend suitable career paths using Machine Learning.
- Help users explore career opportunities.
- Provide career roadmaps for skill development.
- Maintain a history of previous career predictions.
- Connect users with job opportunities.

## ✨ Features

### 👤 User Module
- User Registration and Login
- Forgot Password functionality
- User Profile Management
- Profile Photo Upload

### 🤖 Career Prediction
- Machine Learning-based career recommendation
- Career prediction results
- Prediction History

### 📊 Dashboard
- Career activity overview
- Prediction information
- Graphical data visualization

### 🗺️ Career Roadmap
- Career learning guidance
- Step-by-step skill development

### 💼 Job Module
- Browse job opportunities
- View job details
- Submit job applications

### 🛡️ Admin Module
- Admin Login
- Manage Users
- Manage Job Listings
- View Career Predictions
- Manage Job Applications

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Flask | Backend web framework |
| Machine Learning | Career prediction |
| Scikit-learn | Machine Learning tools |
| Pandas | Data processing |
| NumPy | Numerical operations |
| MySQL | Database management |
| HTML | Web page structure |
| CSS | Web page styling |
| JavaScript | Frontend interactions |
| SMTP | Password reset emails |

## ⚙️ Project Architecture

1. The user registers and logs in.
2. The user provides career-related information.
3. Flask sends the input to the Python backend.
4. The trained Machine Learning model predicts a suitable career.
5. The result is displayed on the website.
6. Prediction information is stored in MySQL.
7. Users can explore career roadmaps and job opportunities.

## 📂 Project Structure

```text
AI_Career_Path/
│
├── app.py
├── config.py
├── db.py
├── ml_model.py
├── requirements.txt
│
├── database/
│   └── database.sql
│
├── dataset/
│   └── career_dataset.csv
│
├── model/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── templates/
    ├── admin/
    └── user/
