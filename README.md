# 🚀 AI Career Path – Career Recommendation System

## 📌 About the Project

AI Career Path is a web-based career recommendation system developed using Python, Flask, MySQL, and Machine Learning.

The main objective of this project is to help users identify suitable career opportunities based on their skills, education, interests, and other relevant information.

The application provides career predictions, prediction history, career roadmaps, job opportunities, and job application functionality through a user-friendly web interface.

## 🎯 Project Objectives

- Recommend suitable careers using Machine Learning.
- Help users explore different career opportunities.
- Provide career roadmaps for skill development.
- Maintain a history of previous career predictions.
- Display job opportunities and job details.
- Allow users to apply for jobs through the application.
- Provide an administration panel to manage application data.

## ✨ Features

### 👤 1. User Authentication
- User registration and login.
- Password hashing for improved security.
- Forgot Password functionality using email.
- Separate admin login.

### 📊 2. Dashboard
- Overview of career prediction activity.
- Display of previous predictions.
- Graphical representation of career information.
- Quick access to application features.

### 👩‍💻 3. User Profile
- View and update personal information.
- Manage education, skills, and interests.
- Upload a profile photo.

### 🤖 4. Career Prediction
- Machine Learning-based career recommendations.
- Prediction results based on user input.
- Integration of the prediction model with the Flask backend.

### 📜 5. Prediction History
- View previous career predictions.
- Store prediction information in the database.

### 🗺️ 6. Career Roadmap
- Career-related learning guidance.
- Step-by-step skill development recommendations.

### 💼 7. Job Opportunities
- Browse available jobs.
- View company and job information.
- Check required skills and qualifications.
- View detailed job descriptions.

### 📝 8. Job Applications
- Apply for available jobs.
- Submit applicant information.
- Upload a resume.
- Track application status where supported.

### 🛡️ 9. Admin Panel
- View registered users.
- Manage job listings.
- View career predictions.
- Manage job applications.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Flask | Backend web framework |
| Machine Learning | Career recommendation |
| Scikit-learn | Machine Learning tools |
| Pandas | Data processing |
| NumPy | Numerical operations |
| MySQL | Database management |
| HTML | Web page structure |
| CSS | Web page styling |
| JavaScript | Frontend interactions |
| SMTP | Password reset emails |
| Git and GitHub | Version control and project hosting |

## 🧠 Machine Learning Approach

The project uses a trained Machine Learning model to predict suitable career categories from user-related input data.

### Prediction Workflow

1. The user enters the required career-related information.
2. The Flask backend receives the input.
3. Python processes the information into the format required by the model.
4. The trained Machine Learning model generates a career prediction.
5. The predicted result is displayed to the user.
6. Prediction details are stored in the MySQL database.

**Note:** The exact algorithm depends on the implementation in `ml_model.py`. Refer to that file for the specific model used in this project.

## 🏗️ Project Architecture

The application consists of three main components:

### 1. Frontend
HTML, CSS, and JavaScript provide the user interface and interactive pages.

### 2. Backend
Python and Flask handle requests, authentication, career predictions, and communication between the frontend and database.

### 3. Database and Machine Learning
MySQL stores application information, while the trained Machine Learning model generates career recommendations.

## 📂 Project Structure

The following is an illustrative project structure. Actual filenames and folders may differ.

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
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   ├── admin/
│   └── user/
│
├── model/
│
├── .gitignore
└── README.md
```

## 💻 How to Run the Project

Follow the steps below to run AI Career Path on your local computer.

### Prerequisites

Install the following software:

- Python
- MySQL Server
- Git
- A code editor such as Visual Studio Code

### Step 1: Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/Nikita-2404/AI-Career-Path.git
```

### Step 2: Open the Project Folder

```bash
cd AI-Career-Path
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```cmd
venv\Scripts\activate
```

### Step 5: Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Step 6: Configure the Database

1. Install and start MySQL Server.
2. Create the database required by the application.
3. Execute the SQL script from the `database` folder, if provided.
4. Configure the database host, username, password, and database name using the configuration method expected by the application.
5. Ensure the application can connect to MySQL.

Do not upload database passwords or other private credentials to GitHub.

### Step 7: Configure Environment Variables

If the application uses a `.env` file, create it locally and add the configuration required by your project.

For example:

```env
SECRET_KEY=replace_with_a_secure_secret_key
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=your_database_name
```

**Important:** These variable names are examples. Check `config.py`, `db.py`, and `app.py` to confirm the exact variable names required by your implementation.

Keep the `.env` file private and do not upload it to GitHub.

### Step 8: Prepare the Machine Learning Model

The trained `model.pkl` file is not included in this repository because it exceeds GitHub's standard file size limit.

Before running the application, check how `ml_model.py` loads the trained model.

If a trained model is required, generate it using the project's training code or place a compatible model in the expected local path.

The model's input features and preprocessing must match the implementation used during training.

### Step 9: Run the Application

Start the Flask application:

```bash
python app.py
```

### Step 10: Open the Application

Open your web browser and visit:

http://127.0.0.1:5000/

The application should open if the dependencies, database, environment variables, and required Machine Learning model are configured correctly.

Through this project, I gained practical experience in:

- Python application development.
- Flask web application development.
- MySQL database integration.
- Machine Learning model integration.
- Frontend development using HTML, CSS, and JavaScript.
- User authentication and application security.
- Git and GitHub version control.

## 👩‍💻 Author

**Nikita Memane**

GitHub: [Nikita-2404](https://github.com/Nikita-2404)

## 🔗 Project Repository

[AI Career Path – GitHub Repository](https://github.com/Nikita-2404/AI-Career-Path)

## 📄 License

This project was developed for educational and portfolio purposes.
