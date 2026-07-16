# Mile Tracker

A Flask-based mileage tracking application that allows users to log and view their running activities. The application supports multiple users, activity filtering, and photo uploads.

## Features

- User selection for personalized tracking
- Log running/walking activities
- Track mileage and dates
- Filter activities by type
- View uploaded photos
- Session-based access control

## Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS
- Jinja Templates

## Project Structure

kwooby-site/
│
├── app.py
├── requirements.txt
├── templates/
├── static/
│ ├── css/
│ └── images/
└── .env

## Database

This project uses SQLite for data storage.

The database contains tables for:

Users
Logged activities
Uploaded photos

During development, if database structure changes, the local database may need to be recreated.

## Future Improvements

Full user authentication system
User account creation
Improved photo management
Additional statistics and charts
Deployment improvements

## Author

Alex Davis
