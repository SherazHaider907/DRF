Product & Order Management Backend

This is a robust product and order management backend built with Django and Django REST Framework (DRF). The project demonstrates a fully functional API with authentication, filtering, caching, async tasks, and scalable architecture.

Features

Custom User System

Extends Django’s AbstractUser

Staff/admin roles and permissions

JWT authentication (access & refresh tokens)

Product & Order Management

Product model with stock management and validation

Order system with UUID primary keys

OrderItem as a through table linking Orders and Products

Nested serializers for creation and updates

Atomic transactions for data integrity

API Functionality

CRUD for products and orders

Filtering, searching, and ordering

Pagination with LimitOffsetPagination

Scoped throttling for rate-limiting

Cache optimization with Redis and Django signals

Background processing using Celery for order confirmation emails

Admin & Testing

Admin panel with inlines for orders and items

Unit tests for permissions, product management, and order retrieval

Documentation

OpenAPI schema generated with drf-spectacular

Swagger UI & Redoc UI for API exploration

Tech Stack

Backend: Django, Django REST Framework

Database: SQLite (development)

Caching & Broker: Redis

Async Tasks: Celery

Authentication: JWT (Simple JWT)

API Documentation: drf-spectacular

Testing: Django TestCase & DRF APITestCase

Project Structure
api/
├── models.py          # User, Product, Order, OrderItem models
├── serializers.py     # DRF serializers for models
├── views.py           # API Views & ViewSets
├── urls.py            # API routes & router
├── filters.py         # Custom filters for Products & Orders
├── signals.py         # Signals for cache invalidation
├── tasks.py           # Celery async tasks
├── tests.py           # Unit tests for models and APIs

drf_course/
├── settings.py        # Project settings (JWT, Celery, Cache, DRF)
├── urls.py            # Main URLs with admin, JWT, API schema
├── wsgi.py
├── asgi.py

Installation

Clone the repository:

git clone https://github.com/yourusername/product-order-backend.git
cd product-order-backend


Create a virtual environment:

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows


Install dependencies:

pip install -r requirements.txt


Apply migrations:

python manage.py migrate


Create superuser:

python manage.py createsuperuser


Run the development server:

python manage.py runserver

Usage

Access admin panel at http://127.0.0.1:8000/admin/

Use API endpoints:

GET /products/ – list products

POST /products/ – create product (admin only)

GET /orders/ – list orders (authenticated users)

POST /orders/ – create order

GET /api/schema/swagger-ui/ – API documentation

JWT tokens for authentication:

POST /api/token/ – obtain access/refresh

POST /api/token/refresh/ – refresh token

Testing

Run tests using:

python manage.py test


This includes:

User authentication & permissions

Product CRUD

Order creation & retrieval
