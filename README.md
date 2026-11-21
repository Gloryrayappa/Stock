# StockWise

StockWise is a Django inventory management application for managing product categories, suppliers, products, stock levels, billing snapshots, accounts, and Django administration.

## Features

- Welcome inventory dashboard
- Add, update, delete, and search stock records
- Low-stock status and reorder-level tracking
- Category management
- Product management
- Supplier management
- Inventory value snapshot for billing
- User signup and Django login
- Styled Django administration dashboard

## Project Structure

- `accounts/` - account views
- `billing/` - billing view
- `inventory/` - stock models and inventory operations
- `products/` - category and product models and operations
- `suppliers/` - supplier models and operations
- `stockwise/` - Django project settings and URLs
- `templates/` - HTML templates

## Requirements

- Python 3.15
- Django 6.1.3

## Setup

```bash
# Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Install Django
pip install django

# Apply database migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Application URLs

| Page | URL |
|---|---|
| Inventory | `http://127.0.0.1:8000/` |
| Categories | `http://127.0.0.1:8000/categories/` |
| Products | `http://127.0.0.1:8000/products/` |
| Suppliers | `http://127.0.0.1:8000/suppliers/` |
| Billing | `http://127.0.0.1:8000/billing/` |
| Accounts | `http://127.0.0.1:8000/accounts/` |
| Create account | `http://127.0.0.1:8000/signup/` |
| Administration | `http://127.0.0.1:8000/admin/` |

## Django Admin

Create an administrator account:

```bash
python manage.py createsuperuser
```

Then open `http://127.0.0.1:8000/admin/` and sign in.

## Development Checks

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py migrate
```
