# Glassly 🕶️

A full-stack e-commerce web application for an eyewear small business, built with Django. Customers can browse glasses, add to cart and place orders via WhatsApp — no account required.

## Live Demo
[View Live](https://ginyboy.pythonanywhere.com/)

---

## Features
- Product catalog with category filtering and search
- Session-based shopping cart (no login required)
- WhatsApp checkout with pre-filled order message
- Dynamic shipping calculation based on delivery area
- Order management via Django admin
- Responsive design with Bootstrap 5

---

## Tech Stack
- **Backend:** Python, Django
- **Frontend:** HTML, CSS, Bootstrap 5
- **Database:** PostgreSQL
- **Deployment:** PythonAnywhere

---

## Installation

```bash
# Clone the repo
git clone https://github.com/godsonginika/glassly.git
cd glassly

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env and add your values

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

---

## Environment Variables
Create a `.env` file in the root directory with the following:
```
SECRET_KEY=your-secret-key
DEBUG=True
WHATSAPP_NUMBER=2348012345678
```
---

## Project Structure
```
Glassly/
├── core/           # Project settings & urls
├── store/          # Product catalog & homepage
├── cart/           # Session-based cart
├── orders/         # Checkout & WhatsApp integration
├── templates/      # HTML templates
├── static/         # CSS, JS, images
└── media/          # Uploaded product images
```

---

## Author
**Your Name**
[GitHub](https://github.com/godsonginika) | [LinkedIn](linkedin/in/godsonginika)

---

## License
MIT License
