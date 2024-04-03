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
  - Registering Process:
    
     https://github.com/Omarkhaled711/infinite-goods/assets/77131348/90da0c3b-7c78-4726-bdb8-0692e37946b0

  - Login Process:
    
    https://github.com/Omarkhaled711/infinite-goods/assets/77131348/690b45ae-2b6f-4845-a677-c82e39401c6c

- **Searching For Products**: Easy-to-use interface for Searching for products based on product name and description

    https://github.com/Omarkhaled711/infinite-goods/assets/77131348/46897db6-2cb6-4951-ab65-29c5dd469f00

- **Cart Functionality**: Seamless shopping cart experience enabling users to add, remove, and modify items before proceeding to checkout.
  - Add To Cart:

    https://github.com/Omarkhaled711/infinite-goods/assets/77131348/594a17bd-c666-491b-93e3-ea9f3bcd39dd

  - Increment, Decrement, and Remove from cart:

    https://github.com/Omarkhaled711/infinite-goods/assets/77131348/b1677f4d-4ce9-4376-99af-86db73dff96b

- **Coupon Application**: Capability to apply discount coupons during checkout, enhancing customer satisfaction and encouraging repeat purchases.

  https://github.com/Omarkhaled711/infinite-goods/assets/77131348/62e2081c-576e-494e-9059-6f3610d687c1
  
- **Place Order Process**: Smooth and intuitive placing order process

  https://github.com/Omarkhaled711/infinite-goods/assets/77131348/94ad0b5e-71f0-4578-9fd5-724ce56ad2a6

- **Payment Integration with PayPal**: Integration with PayPal for secure and convenient online payments, ensuring trust and reliability for customers.

  https://github.com/Omarkhaled711/infinite-goods/assets/77131348/f46515e5-6ca3-47f6-a53f-6adcb6ebff4b

- **Submit Reviews** : Let the people konow what you think of the products you bought, and whether you recommend it or not.

  https://github.com/Omarkhaled711/infinite-goods/assets/77131348/ddd65269-a4ed-48a6-8a44-19f653a9218d

- **Order Management**: Receiving an email when order is completed, and getting updated about the status of your order.
   <details>
     <summary>Click to view screenshot</summary>
     
  ![Order_Confirmation_Mail](https://github.com/Omarkhaled711/infinite-goods/assets/77131348/4d2af1c7-7d04-4124-a515-5835ddf54e96)
  
   </details>

- **Admin Dashboard**: Granting superuser access to monitor and manage data according to administrative preferences.
   <details>
     <summary>Click to view screenshot</summary>
     
  ![admin_dashBoard](https://github.com/Omarkhaled711/infinite-goods/assets/77131348/a9f3716e-a1b5-489a-92e3-9529f5d02440)

  </details>

And More... We are Continuously evolving features to improve the overall shopping experience and meet the diverse needs of our customers.

## REST API
We provide a RESTful API to interact with various resources. Below are the available endpoints for now:

### Product Endpoints

- **GET /shop/api/v1/products/**
  - Description: Retrieve a list of all products available in the shop.
  - Parameters: None
- **GET /shop/api/v1/products/{product_id}/**
  - Description: Retrieve details of a specific product by its ID.
  - Parameters:
    - {product_id}: Unique identifier of the product.

### Category Endpoints

- **GET /category/api/v1/categories/**:
  - Description: Retrieve a list of all categories.
  - Parameters: None

### Cart Items Endpoint

- **GET /cart/api/v1/cart/items/**
  - Description: Retrieve the items currently in the user's shopping cart.
  - Authentication: Supports both Session Authentication and Token Authentication.
  - Parameters: None

### Order Endpoints

- **GET /orders/api/v1/orders/**
  - Description: Retrieve a list of all orders placed by the current user.
  - Authentication: Supports both Session Authentication and Token Authentication.
  - Method: GET
  - Parameters: None

- **POST /orders/api/v1/orders/**
  - Description: Place a new order.
  - Authentication: Supports both Session Authentication and Token Authentication.
  - Method: POST
  - Parameters: Order details (e.g., products, quantities)

- GET /orders/api/v1/orders/{order_id}/
  - Description: Retrieve details of a specific order by its ID.
  - Authentication: Supports both Session Authentication and Token Authentication.
  - Method: GET
  - Parameters:
    - {order_id}: Unique identifier of the order.

## Requirements

Ensure you have the packages inside requirements.txt installed.

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
