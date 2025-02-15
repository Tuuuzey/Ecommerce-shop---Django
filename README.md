E-commerce Website
Technologies Used:
Django (version 4.2.7)
Python (version 3.11)
Jinja (version 3.1.2)
HTML (5)
CSS (3)
Bootstrap (version 5.3.0)
JavaScript (ES6)
PostgreSQL (version 15.2)
Features Implemented:
Advanced Full-Functional E-commerce Website
User Authentication: Login and sign-up system
Shopping Cart: Add products to cart and manage items
User Profile: Users can update their email, with email verification link sent to confirm the change
Checkout: Fully functional checkout process (without real money transactions), integrated with Stripe for payment processing
Product Comments and Ratings: Users can leave comments and rate products
Wishlist: Save products to your wishlist
Seller Features: Users can become a seller, manage their own products, and edit product details
API:
API endpoints for products, product details, creating users
API documentation
CRUD Operations:
Create users, sellers, products, promo codes, shipping addresses, transactions, orders, and order items
Model String Representation: Correct implementation of the __str__ method for models to improve readability in the Django admin and elsewhere
Configuration:
secret_key:
You will need to generate a secret key for Django. You can use the following command to create one:
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

stripe_secret_key_test:
Sign up on Stripe and get your test API key from the Stripe dashboard. Set the key in the .env file as STRIPE_SECRET_KEY_TEST.

Database Configuration (PostgreSQL):

Create a new PostgreSQL database and a user with permissions:
Migrate the database:
All tables have been created and migrations are ready to be applied. Run the following command to apply migrations and set up the database schema:
python manage.py migrate
This will create all the necessary tables and update the database according to the models in your Django project.
Update DATABASES in settings.py with your PostgreSQL credentials:
After creating the database, open the settings.py file in your Django project and find the DATABASES section. Update it with the following values:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',  # or the appropriate host if using a remote database
        'PORT': '5432',  # default PostgreSQL port
    }
}
Replace your_db_name, your_db_user, and your_db_password with the values you used when setting up the PostgreSQL database.
Update DATABASES in settings.py with your PostgreSQL credentials.


Email Configuration (for email verification):

Create a new Gmail account to be used for email verification.
Enable two-factor authentication (2FA) on the Gmail account.
Create an "App Password" for Django to send emails by going to Google Account settings → Security → App passwords.
Add the generated App password to your .env file as EMAIL_PASSWORD.
Install Dependencies:
Install all required Python dependencies by running:
pip install -r requirements.txt