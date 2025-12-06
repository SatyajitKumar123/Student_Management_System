# 🎓 Student Management System (SMS)

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-5.0+-green)
![TailwindCSS](https://img.shields.io/badge/Tailwind-CSS-38bdf8)
![HTMX](https://img.shields.io/badge/HTMX-Realtime-orange)
![Status](https://img.shields.io/badge/Status-Live-success)

A comprehensive, full-stack web application designed to manage student records, track enrollment trends, and visualize data. Built with **Django** and **Tailwind CSS**, featuring **HTMX** for a modern, single-page-application (SPA) feel without the complexity of a frontend framework.

## 🚀 Live Demo

**View the Live Application:** [https://satyajit.pythonanywhere.com](https://satyajit.pythonanywhere.com)

> **Demo Credentials (for recruiters):**
> * **Username:** guest
> * **Password:** guest123

---

## ✨ Key Features

### 📊 Interactive Dashboard
- Real-time data visualization using **Chart.js**.
- Tracks total students, course distribution (Pie Chart), and monthly enrollment trends (Line Chart).

### 🔍 Advanced Search & Filtering (HTMX)
- **Instant Search:** Search by name or enrollment number without reloading the page.
- **Dynamic Filtering:** Filter students by course with preserved state during pagination.
- **HTMX Integration:** Uses AJAX requests to update only the table rows, reducing server load and improving UX.

### 📂 File Management & Optimization
- **Profile Photos:** Students can upload profile pictures.
- **Auto-Compression:** Integrated **Pillow** library to automatically resize and compress images (max 800x800px) upon upload to save server storage and bandwidth.
- **Auto-Cleanup:** Custom Signals (`pre_save`, `post_delete`) ensure old or deleted images are removed from the filesystem to prevent clutter.

### 📱 Fully Responsive Design
- Built with **Tailwind CSS**.
- Features a mobile-friendly **Hamburger Menu**.
- Tables are optimized for small screens with horizontal scrolling.

### 📄 Data Export
- One-click export of student data to **CSV** format for external reporting.

---

## 🛠️ Tech Stack

* **Backend:** Python, Django
* **Frontend:** HTML5, Tailwind CSS (CDN), JavaScript
* **Dynamic Interactions:** HTMX (Hypermedia-driven dynamic UI)
* **Data Visualization:** Chart.js
* **Database:** SQLite (Development/Production for this demo)
* **Deployment:** PythonAnywhere (Linux/Bash environment)

---

## ⚙️ Installation & Local Setup

If you want to run this project locally:

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/SatyajitKumar123/Student_Management_System.git](https://github.com/SatyajitKumar123/Student_Management_System.git)
    cd Student_Management_System
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply Migrations**
    ```bash
    python manage.py migrate
    ```

5.  **Create Superuser**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the Server**
    ```bash
    python manage.py runserver
    ```

Access the app at `http://127.0.0.1:8000/`

---

## 💡 Technical Highlights

* **HTMX over React/Vue:** I chose HTMX to keep the tech stack simple and Python-centric while still achieving a smooth, "no-refresh" user experience for search and pagination.
* **Signal Handling:** Used Django Signals to handle file cleanup, ensuring the application remains storage-efficient over time.
* **Security:** Implemented `LoginRequiredMixin` across views and proper CSRF protection for all forms and HTMX requests.

---

## 👤 Author

**Satyajit**
* [GitHub Profile](https://github.com/SatyajitKumar123)