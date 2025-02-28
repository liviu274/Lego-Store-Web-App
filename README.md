# Lego-Store-Web-App

A Shopify-style full stack web application created using Django.

## Features

### User Authentication
- **Registration**: Users can create an account by providing their details and confirming their email.
- **Login**: Users can log in to their account. The login form includes a "Stay logged in" option.
- **Logout**: Users can log out of their account.
- **Password Change**: Users can change their password.

### User Profile
- **Profile Management**: Users can view their profile details including first name, last name, email, phone, zip code, address, city, and county.
- **Special Offers**: Logged-in users can access special offers.

### Product Management
- **Product Listing**: Products are listed with their names and prices.
- **Product Filtering**: Users can filter products based on name, description, and price range.
- **Product Detail View**: Users can view detailed information about a product, including its name, description, price, and stock quantity.

### Shopping Basket
- **Add to Basket**: Users can add products to their basket.
- **View Basket**: Users can view the contents of their basket, update quantities, and remove items.

### Contact Form
- **Contact Us**: Users can fill out a contact form to send messages to the store. The form includes fields for first name, last name, birth date, email, message type, subject, minimum wait days, and message content.

### Reviews
- **Add Review**: Users can add reviews for products. The review form includes fields for product name, product price, rating, and comment.

### Sales and Special Offers
- **Add Sale**: Admins can create sales for specific product categories. The sale form includes fields for name, description, discount, duration, and categories.
- **Special Offer Page**: Users with special offer permissions can view a special offer page with a 50% discount code.

### Admin Panel
- **Admin Dashboard**: Admins can manage products, categories, users, reviews, orders, and sales through the Django admin panel.

### Email Notifications
- **Registration Confirmation**: Users receive an email to confirm their registration.
- **Sale Notifications**: Users receive email notifications about sales and special offers.

### Logging
- **Logging**: The application logs various events such as user registration, login attempts, form submissions, and errors.

