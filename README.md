# Infinite Goods

Infinite Goods is an e-commerce platform aimed at providing a seamless shopping experience for users interested in purchasing a variety of products online. The platform allows users to browse through a wide range of categories, add products to their cart, and securely complete transactions. It also includes features such as user authentication, product search, applying coupons, and a lot more.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- **User Authentication**: Secure user authentication system allowing customers to create accounts, activate their email through a validating link, login, and manage their profiles.

- **Product Management**: Easy-to-use interface for adding, updating, and deleting products, as well as managing inventory and product attributes.

- **Shopping Cart Functionality**: Seamless shopping cart experience enabling users to add, remove, and modify items before proceeding to checkout.

- **Checkout Process**: Smooth and intuitive checkout process with multiple payment options for a hassle-free purchasing experience.

- **Order Management**: Receiving an email when order is completed, and getting updated about the status of your order.

- **Payment Integration with PayPal**: Integration with PayPal for secure and convenient online payments, ensuring trust and reliability for customers.

- **Coupon Application**: Capability to apply discount coupons during checkout, enhancing customer satisfaction and encouraging repeat purchases.

- **Admin Dashboard**: Granting superuser access to monitor and manage data according to administrative preferences.

And More... We are Continuously evolving features to improve the overall shopping experience and meet the diverse needs of our customers.

## Requirements

Ensure you have the following packages installed:

- asgiref==3.2.10
- Django==3.1
- pillow==10.2.0
- pytz==2024.1
- sqlparse==0.4.4

You can install these dependencies using pip:

```bash
pip install -r requirements.txt
```

Make sure to run this command in your project directory to install all the required packages before running the app.

## Installation

1. Clone the repository: `git clone 'https://github.com/Omarkhaled711/infinite-goods.git'`

2. Navigate to the project directory: `cd infinite-goods`

3. Install dependencies: `pip install -r requirements.txt`

## Configuration

Before running the app, ensure to configure the necessary environment variables found in infiniteGoods/settings.py.

For instance, you'll need to set up the following environment variables:

- **DJANGO_EMAIL**: Set this variable to the email address you wish to use for sending various emails such as verification mails, order received successfully mails, etc.

- **DJANGO_PASS**: Set this variable to the corresponding password for the email account specified in DJANGO_EMAIL.

Make sure to configure these environment variables correctly to enable essential email functionalities within the app.

## Usage

- To simply run the Django app:
  1. `python3 manage.py runserver`
  2. Open your web browser and navigate to <http://127.0.0.1:8000>

- To create a superuser:
  - `python3 manage.py createsuperuser`

- If you edited one of the models, or created a new model:
  1. `python.py manage.py makemigrations`
  2. `python manage.py migrate`

## Contributing

- Fork the repository

- Make your changes

- Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
