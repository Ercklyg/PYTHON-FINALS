
# Gym Fitness Management System

This project is a **Gym Fitness Management System** built using **Tkinter** for the graphical interface and **MySQL** for database management. It provides features for managing gym memberships, user registration, promo selection, and administrative tasks. The system supports distinct functionalities for **users** and **admins**.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
   - [User Features](#user-features)
   - [Admin Features](#admin-features)
3. [Python Concepts and Libraries Used](#python-concepts-and-libraries-used)
4. [Prerequisites](#prerequisites)
5. [Setup Instructions](#setup-instructions)
6. [Database Schema and Setup](#database-schema-and-setup)
7. [Screens and Functionalities](#screens-and-functionalities)
8. [Default Credentials](#default-credentials)
9. [Future Enhancements](#future-enhancements)

---

## Project Overview

The Gym Fitness Management System provides a centralized application to streamline the process of managing gym memberships. Users can register, select membership promos, and view personalized dashboards, while admins can manage user data and monitor membership details.

---

## Features

### User Features
- **User Registration**: Register with a username and password.
- **Promo Selection**: Choose from available promos, each with specific durations and prices.
- **Dashboard Access**: View membership details, including promo information and expiration dates.

### Admin Features
- **Admin Authentication**: Secure login for admins.
- **User Management**: View user details, including promo and expiration information.
- **Receipt Generation**: Generate and view detailed membership receipts.
- **Logout Option**: Secure logout with session cleanup.

---

## Python Concepts and Libraries Used

1. **Tkinter**: Provides the graphical user interface for screens and buttons.
2. **MySQL Connector**: Manages database interactions for authentication, user registration, and data fetching.
3. **Random Module**: Generates unique receipt numbers.
4. **Datetime Module**: Calculates promo expiration dates.

---

## Prerequisites

1. **Python 3.7+**
2. **MySQL Server** with a database named `gym_python`.
3. Python Libraries:
   - `mysql-connector-python`
   - `tkinter`

Install dependencies using:
```bash
pip install mysql-connector-python
```

---

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Set Up Database**:
   - Open your MySQL client and run the following script to create the required tables and sample data:

     ```sql
     -- Create the database
     CREATE DATABASE gym_python;

     -- Use the created database
     USE gym_python;

     -- Create the admins table
     CREATE TABLE admins (
         admin_id INT AUTO_INCREMENT PRIMARY KEY,
         username VARCHAR(50) NOT NULL UNIQUE,
         password VARCHAR(255) NOT NULL
     );

     -- Create the promos table
     CREATE TABLE promos (
         promo_id INT AUTO_INCREMENT PRIMARY KEY,
         promo_name VARCHAR(100) NOT NULL,
         duration_days INT NOT NULL,
         price DECIMAL(10, 2) NOT NULL
     );

     -- Create the users table
     CREATE TABLE users (
         user_id INT AUTO_INCREMENT PRIMARY KEY,
         username VARCHAR(50) NOT NULL UNIQUE,
         password VARCHAR(255) NOT NULL,
         promo_id INT,
         FOREIGN KEY (promo_id) REFERENCES promos(promo_id) ON DELETE SET NULL
     );

     -- Insert sample data into the promos table
     INSERT INTO promos (promo_name, duration_days, price) VALUES
     ('1 DAY', 1, 40.00),
     ('7 DAYS', 7, 220.00),
     ('30 DAYS', 30, 950.00);

     -- Insert sample data into the admins table
     INSERT INTO admins (username, password) VALUES
     ('admin', 'oks');  -- Make sure to hash passwords in a real application

     -- Insert sample data into the users table
     INSERT INTO users (username, password) VALUES
     ('user1', 'password1'),
     ('user2', 'password2');
     ```

3. **Run the Application**:
   ```bash
   python main.py
   ```

4. **Access the Application**:
   - Launch the Tkinter interface for user or admin login.

---

## Database Schema and Setup

### Users Table
| Field       | Type         | Description              |
|-------------|--------------|--------------------------|
| `user_id`   | INT          | Primary key              |
| `username`  | VARCHAR(50)  | Unique username          |
| `password`  | VARCHAR(255) | User password            |
| `promo_id`  | INT          | Foreign key to `promos`  |

### Promos Table
| Field       | Type         | Description              |
|-------------|--------------|--------------------------|
| `promo_id`  | INT          | Primary key              |
| `promo_name`| VARCHAR(100) | Name of the promo        |
| `duration_days` | INT      | Duration in days         |
| `price`     | DECIMAL(10,2)| Promo price              |

### Admins Table
| Field       | Type         | Description              |
|-------------|--------------|--------------------------|
| `admin_id`  | INT          | Primary key              |
| `username`  | VARCHAR(50)  | Admin username           |
| `password`  | VARCHAR(255) | Admin password           |

---

## Screens and Functionalities

This section outlines all the screens and their functionalities, including **Login Screen**, **Admin Dashboard**, and **Promo Selection Screen**. [Details omitted for brevity in this summary; see the main README above.]

---

## Default Credentials

### Admin
- **Username**: `admin`
- **Password**: `oks`

---

## Future Enhancements
- Add password recovery functionality.
- Enhance promo selection with filters for price and duration.
- Integrate analytics for membership trends.
- Implement session management for improved security.

