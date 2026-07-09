# ☕ StarQueen Cafe Management System

A modern and responsive **Cafe Management System** developed using **Python, Django, MySQL, HTML, CSS, and JavaScript**. The application enables customers to browse the menu, reserve tables, explore the cafe gallery, and place home delivery orders through an easy-to-use web interface.

---

# 🚀 Project Overview

The **StarQueen Cafe Management System** is a full-stack web application designed to simplify cafe operations and enhance the customer experience. It provides an attractive user interface for customers while allowing efficient management of menu items, reservations, gallery images, delivery orders, and delivery areas.

---

# ✨ Features

## 🍽️ Menu Management

* Dynamic menu categorized by food type
* Best Seller section
* Food availability management
* Category-wise filtering

## 📅 Table Reservation

* Online table booking
* Customer details collection
* Date & time selection
* Guest count
* Special request support
* Reservation status management

## 🖼️ Gallery

* Cafe Interior Gallery
* Food Gallery
* Customer Gallery
* Image upload support

## 🚚 Home Delivery

* Online food ordering
* Customer delivery details
* Delivery area validation
* Automatic order number generation
* Delivery charge calculation
* Order confirmation page

## 📦 Order Tracking

* Track order using Order ID
* Order status updates
* Complete order summary

## 📍 Delivery Area Management

* Delivery area configuration
* Pincode-based delivery
* Minimum order validation
* Delivery charge management

---

# 🛠️ Technology Stack

### Backend

* Python
* Django

### Database

* MySQL

### Frontend

* HTML5
* CSS3
* JavaScript

### Django Features Used

* Django ORM
* Models
* Views
* URL Routing
* Forms
* Template Inheritance
* Static Files
* Media Files
* Messages Framework
* Authentication-ready Architecture

---

# 📂 Project Structure

```text
starqueen_v2/
│
├── cafe/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
│
├── starqueen/
│   ├── settings.py
│   ├── urls.py
│   ├── templates/
│   │   └── cafe/
│   └── wsgi.py
│
├── static/
│   ├── cafe/
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
│
├── media/
├── manage.py
└── requirements.txt
```

---

# 🗄️ Database Models

The project contains the following database models:

* MenuItem
* Reservation
* GalleryImage
* DeliveryOrder
* OrderItem
* DeliveryArea

---

# ⚙️ Installation

## Clone the Repository

```bash
git clone https://github.com/Omkar4682/starqueen_v2.git
```

```bash
cd starqueen_v2
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🗄️ Configure MySQL Database

Update the `DATABASES` section in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

---

## Apply Migrations

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

---

## Create Superuser

```bash
python manage.py createsuperuser
```

---

## Run the Development Server

```bash
python manage.py runserver
```

Open your browser and visit:

```text
http://127.0.0.1:8000/
```

---

# 📷 Main Modules

* Home
* Menu
* Gallery
* Events
* Visit Us
* Table Reservation
* Home Delivery
* Order Confirmation
* Order Tracking

---

# 🎯 Learning Outcomes

This project demonstrates practical knowledge of:

* Django Framework
* MySQL Database Integration
* Django ORM
* CRUD Operations
* Model Relationships
* Form Handling & Validation
* Template Inheritance
* Static & Media File Management
* Session Management
* Responsive Web Design
* MVC (MVT) Architecture in Django

---

# 🚀 Future Enhancements

* User Authentication
* Online Payment Gateway
* Email Notifications
* SMS Notifications
* Customer Dashboard
* Admin Analytics Dashboard
* Offers & Coupons
* Reviews & Ratings
* Wishlist
* Search & Filter
* Invoice Generation

---

# 👨‍💻 Author

**Omkar Date**

**GitHub:** https://github.com/Omkar4682

**LinkedIn:** https://www.linkedin.com/in/omkar-date-04969435b

---

# 📄 License

This project is developed for educational, learning, and portfolio purposes.
