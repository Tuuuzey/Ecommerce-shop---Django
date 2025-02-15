# E-commerce Website Documentation

A comprehensive guide for setting up and configuring your advanced e-commerce platform.

---

## Technologies Used

- **Django** (version 4.2.7)
- **Python** (version 3.11)
- **Jinja** (version 3.1.2)
- **HTML** (5)
- **CSS** (3)
- **Bootstrap** (version 5.3.0)
- **JavaScript** (ES6)
- **PostgreSQL** (version 15.2)

---

## Features Implemented

- **Advanced Full-Functional E-commerce Website**
  - **User Authentication:** Login and sign-up system.
  - **Shopping Cart:** Add products to cart and manage items.
  - **User Profile:** Update email with a verification link sent to confirm changes.
  - **Checkout:** Fully functional process (without real money transactions) integrated with Stripe for payment processing.
  - **Product Comments and Ratings:** Leave comments and rate products.
  - **Wishlist:** Save products to your wishlist.
  - **Seller Features:** Become a seller, manage products, and edit product details.

---

## API

- **Endpoints for:**
  - Products
  - Product details
  - User creation
- **Documentation:** Comprehensive API documentation is provided.

---

## CRUD Operations

- **Create:** Users, sellers, products, promo codes, shipping addresses, transactions, orders, and order items.
- **Model String Representation:** Proper implementation of the `__str__` method for better readability in the Django admin and other interfaces.

---

## Configuration

### Secret Keys

- **Django Secret Key:**  
  Generate a secret key by running:
  ```bash
  python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

## Configuration

### Stripe Secret Key (Test)

1. Sign up on [Stripe](https://stripe.com) and get your test API key from the Stripe dashboard.
2. Set the key in your `.env` file as (or in settings.py):
   ```env
   STRIPE_SECRET_KEY_TEST=your_stripe_test_key
## Database Configuration (PostgreSQL)

1. **Create a New PostgreSQL Database**  
   Create a new PostgreSQL database and a user with the necessary permissions.

2. **Migrate the Database**  
   Run the following command to apply migrations and set up the database schema:
   ```bash
   python manage.py migrate
This command will create all the necessary tables and update the database according to the models in your Django project.

### Update `DATABASES` in `settings.py` with Your PostgreSQL Credentials

1. After creating the database, open the `settings.py` file in your Django project.
2. Find the `DATABASES` section and update it with the following values:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_db_name',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': 'localhost',  # or the appropriate host if using a remote database
           'PORT': '5432',       # default PostgreSQL port
       }
   }
### Update `DATABASES` in `settings.py` with Your PostgreSQL Credentials

1. Replace `your_db_name`, `your_db_user`, and `your_db_password` with the credentials you used when setting up the PostgreSQL database.
   
---

## Email Configuration (for Email Verification)

Follow the steps below to set up email verification:
### Email Configuration (for Email Verification)

1. **Create a New Gmail Account**  
   Create a new Gmail account to be used for email verification.

2. **Enable Two-Factor Authentication (2FA)**  
   Enable 2FA on the Gmail account.

3. **Create an App Password for Django**  
   - Go to Google Account settings → **Security** → **App passwords**.
   - Generate an "App Password" to be used by Django for sending emails.

4. **Set the App Password in `.env` File**   
   Add the generated app password to your `.env` file as (or in settings.py):
   ```env
   EMAIL_PASSWORD=your_app_password
### Install Dependencies

To install all required Python dependencies, run the following command:
```bash
pip install -r requirements.txt
