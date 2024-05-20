# MRP Lite

MRP Lite is an ongoing development project aimed at providing a lightweight and easy-to-use Material Requirements Planning (MRP) system built with Django and AdminLTE.

## Purpose

MRP Lite is designed to simplify the process of managing material requirements for small manufacturing businesses. It offers essential MRP functionalities in a user-friendly interface, making it accessible to users with varying levels of technical expertise.

## Current Features
- Comprehensive inventory tracking
- CRUD operations for inventory items and item groups
- User authentication and protected page access
- Responsive design with Admin-LTE Theme
- Advanced search and filter capabilities

## Getting Started

### Clone the Repository

1. Begin by cloning the project repository from GitHub:
  ```bash
  git clone https://github.com/alyssawalter/mrplite
```
### Install Dependencies
1. Make sure Python and pip are installed on your system.
2. Navigate to the project directory in the terminal or command prompt and create a virtual environment:
 ```bash
 python -m venv myenv
 source myenv/bin/activate  # For Unix/Linux
 myenv\Scripts\activate      # For Windows
 ```
3. Install the required dependencies:
  ```bash
  pip install -r requirements.txt
  ```
### Setting up the Database
1. Although the project was originally developed with PostgreSQL, it's recommended to use SQLite for simplicity. Update the settings.py file as follows:
```python
# mrplite/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
2. Apply database migrations by running:
```bash
python manage.py makemigrations
python manage.py migrate
```
### Collect Static Files
Collect static files required:
```bash
python manage.py collectstatic
```
### Run the Development Server
Start the Django development server:
```bash
python manage.py runserver
```
Access the project in your web browser by navigating to http://localhost:8000.

## Note
MRP Lite is currently under ongoing development. Some features may be incomplete or subject to change.
