# Django Recipe Management System

A comprehensive Django web application for managing recipes with user authentication.

## Features

- User authentication (login/logout)
- Recipe management with ingredients
- Professional UI with glass-morphism design
- Responsive design for mobile and desktop
- Image support for recipes
- Difficulty calculation based on ingredients and cooking time

## Quick Start

1. Install dependencies:
   ```bash
   pip install django pillow
   ```

2. Run migrations:
   ```bash
   python manage.py migrate
   ```

3. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

4. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Project Structure

- `recipes/` - Main recipe application
- `ingredients/` - Ingredients management
- `users/` - User management
- `media/` - Uploaded images and static files
- `recipe_project/` - Django project settings

## Authentication

The application includes a complete authentication system with:
- Professional login page with background image
- Logout functionality
- Protected views requiring authentication
- User session management

Access the application at `http://127.0.0.1:8000/`