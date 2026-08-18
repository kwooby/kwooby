# Mile Tracker

A full-stack mileage tracking web application built with **Flask** and **PostgreSQL** that allows users to record, organize, and manage their running and walking activities. The application features secure authentication, cloud-based photo storage, filtering tools, and a responsive interface designed for both desktop and mobile devices.

---

## Features

### User Accounts

* Secure user registration and login
* Session-based authentication
* Password hashing for account security
* Protected user-specific data
* Account settings

### Activity Tracking

* Log running and walking activities
* Record mileage and activity dates
* Dashboard displaying recent activity
* View complete activity history
* Filter activities by type and year
* Delete logged activities

### Photo Gallery

* Upload activity photos
* Cloud-hosted image storage with Cloudinary
* Paginated photo gallery
* Delete uploaded photos

### User Experience

* Responsive design for desktop and mobile
* Clean and intuitive interface
* Organized dashboard for quick access to recent activity

---

## Tech Stack

### Backend

* Python
* Flask
* PostgreSQL
* Psycopg

### Frontend

* HTML5
* CSS3
* Jinja Templates
* JavaScript

### Cloud & Deployment

* Cloudinary
* Render

---

## Database

The application uses PostgreSQL to manage application data.

Current tables include:

* Users
* Activities
* Photos

Passwords are securely hashed before storage.

Uploaded images are stored in Cloudinary, while their secure URLs are saved in PostgreSQL.

---

## Authentication

The application uses Flask sessions to manage authentication.

Authenticated users can:

* Create an account
* Log in and log out securely
* Access only their own activities and uploaded photos
* Manage their personal data through the settings page

---

## Future Improvements

* Interactive charts and mileage statistics
* Goal setting and progress tracking
* Personal records and achievements
* Search and advanced sorting
* Password reset functionality
* REST API for activity data
* Additional user customization options

---

## Author

**Alex Davis**

Built as a personal portfolio project while learning full-stack web development and expanding my experience with Flask, PostgreSQL, and modern web technologies.
