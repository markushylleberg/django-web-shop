# django-web-shop

## An E-commerce site build with the Django framework. 

### Details

#### shop app
- This web shop can handle a large number of products - simply because each product can have multiple product variants, and each product variant can have multiple product variant attributes.

- This web shop is dynamical in the sense that it builds its search function and categories based on the values in the database.

- You can sign up as a user and place an order, view all your placed orders, manage your wishlist, manage your cart and much more.

#### account app
- A full working account app is build alongside the shop app that can handle
  1) sign up/login process
  2) new password requests on mail
  3) change all user information when signed in
  4) change password / delete account

### API

There is an API connected to this project where you can fetch and manipulate the invoices of the system. This would be relevant if the owners of the django-web-shop would build their own system eg. for the warehouse managers to pack the orders and mark them as 'packed' or 'shipped'.
