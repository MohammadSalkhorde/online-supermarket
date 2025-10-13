# 🛒 Online Supermarket - SuperShop

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.0-success?logo=django)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow?logo=javascript)
![License](https://img.shields.io/badge/License-MIT-yellow)

SuperShop is a **full-featured online supermarket platform** built with **Django**, providing user registration, shopping cart, product management, and order tracking.
This project is designed as a **learning platform** and also as a base for real-world e-commerce development.

---

## 🚀 Key Highlights

* Modular architecture using Django
* User registration and SMS-based authentication
* Shopping cart and order process
* Product management with categories and attributes
* Customer user panel and admin panel

---

## 🧠 Technologies

* **Backend:** Python, Django
* **Frontend:** HTML, CSS, JavaScript
* **Database:** MySQL

---

## ⚙️ Features

### 👤 User Panel

* User registration & login
* SMS-based authentication
* Profile management
* View and track orders
* Shopping cart

### 🛒 Product Management

* Products in specific categories with defined attributes
* Search and filter products
* View product details
* Rate products
* Add comments/reviews

### 💳 Orders & Payment

* Place product orders
* Track order status

### 🛠️ Admin Panel

* Manage products, categories, orders, and users

---

## 🧩 Installation & Setup

### 1️⃣ Clone the project

```bash
git clone https://github.com/MohammadSalkhorde/supershop.git
cd supershop
```

### 2️⃣ Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure the database

Set your database credentials in `.env` or `settings.py`:

```
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=3306
```

### 5️⃣ Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ Run the development server

```bash
python manage.py runserver
```

> Access the application at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 📁 Project Structure

```
supershop/
│
├── shop/
│   ├── apps/
│   ├── static/
│   ├── media/
|   ├── shop/
|   ├── middlewares/ 
|   ├── manage.py
|   ├── utils.py
│   └── templates/
│
├── venv/
├── .gitignore
├── README.md
├── .env.example
└── requirements.txt
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 💼 Contact & Portfolio

Hi, I'm **Mohammad Salkhorde** 👋
**Python / Django Backend Developer** — building web applications and APIs.

* **GitHub:** [https://github.com/MohammadSalkhorde](https://github.com/MohammadSalkhorde)
* **LinkedIn:** [https://www.linkedin.com/in/mohammad-salkhorde-a13767385](https://www.linkedin.com/in/mohammad-salkhorde-a13767385)
* **Portfolio:** [https://mohammad-salkhorde.ir](https://mohammad-salkhorde.ir)
* **Email:** [m.salkhorde444@gmail.com](mailto:m.salkhorde444@gmail.com)
