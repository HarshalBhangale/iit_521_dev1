# MAD1_GRocery Store Project 

## General
This is a Flask-based web application with functionalities that include Grocery Store management and Marketplace .
The application integrates with  SQLite database using Flask-SQLAlchemy and provides secure authentication using Flask-Login and Werkzeug.
As mentioned No Css has been used , Only Bootstrap and Jinja has been used in the html templates


## Prerequisites
- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Werkzeug
- Matplotlib
- Numpy

While Developing the project , Was getting some errors so I avoided using Venv , as a result many unnecessary requirements have been added .. 

## Setting Up

1. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

2. Run the application:
    ```bash
    python app.py
    ```
## Problems I faced and is Still working On :: 
- Solved : Creating a Unique Cart for each User
- ## Remaining:
    - 1. Using Cascade in SQL to delete all the products with the categories , 
    Right now ,each product is needed to removed first before deleting each category 
    - 2. Api's not working
    - 3. No css used , So not great styling !! 
    - 4. Minor Bugs might present.
    - 5. entire Code is in one app.py which is Horrible , But I tried to make it as good as possible 
    by adding Comments and lines between each independent functions

## Database Models
- ### 1. User
- **Attributes**:
  - `id`: Unique identifier.
  - `username`: Unique username of the user.
  - `password`: Hashed password for authentication.
- **Relationships**:
  - `cart_items`: Related items from the CartItem model.
  
### 2. Product
- **Attributes**:
  - `id`: Unique identifier.
  - `name`: Name of the product.
  - `unit`: Measurement unit of the product.
  - `price_per_unit`: Price per individual unit.
  - `stock_quantity`: Current stock quantity.
- **Relationships**:
  - `cart_items`: Related items from the CartItem model.
  - `category`: Associated category from the Category model.

### 3. CartItem
- **Attributes**:
  - `id`: Unique identifier.
  - `user_id`: Related user identifier.
  - `product_id`: Related product identifier.
  - `quantity`: Quantity of the product in the cart.
- **Relationships**:
  - `user`: Associated user from the User model.
  - `product`: Associated product from the Product model.
  - `cart`: Associated cart from the Cart model.
- **Methods**:
  - `calculate_total_price`: Calculates the total price for this cart item.

### 4. Cart
- **Attributes**:
  - `id`: Unique identifier.
  - `user_id`: Related user identifier.
- **Relationships**:
  - `cart_items`: Related items from the CartItem model.

### 5. Category
- **Attributes**:
  - `id`: Unique identifier.
  - `name`: Name of the category.
- **Relationships**:
  - `products`: Associated products from the Product model.

### 6. Review
- **Attributes**:
  - `id`: Unique identifier.
  - `user_id`: Related user identifier.
  - `product_id`: Related product identifier.
  - `content`: Review content.
- **Relationships**:
  - No direct relationships in the provided snippet.


## Routes

## 1. STORE MANAGER ROUTES
### 1. User Loader
- **Endpoint**: Internal use for Flask-Login
- **Purpose**: Fetches a user from the database using their ID.

### 2. Manager Login
- **Endpoint**: `/`
- **Methods**: `GET`, `POST`
- **Purpose**: Renders login page and checks credentials.

### 3. Manager Dashboard
- **Endpoint**: `/dashboard`
- **Methods**: `GET`, `POST`
- **Purpose**: Displays all product categories.

### 4. Add Category
- **Endpoint**: `/add-category`
- **Methods**: `POST`
- **Purpose**: Adds a new category.

### 5. Delete Category
- **Endpoint**: `/delete-category/<int:category_id>`
- **Purpose**: Deletes a category.

### 6. Edit Category
- **Endpoint**: `/edit-category/<int:category_id>`
- **Methods**: `GET`, `POST`
- **Purpose**: Fetches category for editing or updates it.

### 7. Add Product
- **Endpoint**: `/add-product/<int:category_id>`
- **Methods**: `POST`
- **Purpose**: Adds a new product to a category.

### 8. Edit Product
- **Endpoint**: `/edit-product/<int:product_id>`
- **Methods**: `GET`, `POST`
- **Purpose**: Fetches product for editing or updates it.

### 9. Delete Product
- **Endpoint**: `/delete-product/<int:product_id>`
- **Purpose**: Deletes a product.

### 10. Logout
- **Endpoint**: `/logout`
- **Purpose**: Logs the user out.

### 11. Summary
- **Endpoint**: `/summary`
- **Purpose**: Provides a visual summary of sales, products, and user activity.

## USER Dashboard ROUTES

### 1. User Login
- **Endpoint**: `/user_login`
- **Methods**: `GET`, `POST`
- **Purpose**: Handles user login. Redirects if already authenticated.

### 2. User Registration
- **Endpoint**: `/user_register`
- **Methods**: `GET`, `POST`
- **Purpose**: Handles user registration. Redirects if already authenticated.

### 3. User Dashboard
- **Endpoint**: `/user_dashboard`
- **Methods**: `GET`
- **Purpose**: Displays available products and categories, allows for product search and sorting.

### 4. Buy Product
- **Endpoint**: `/buy-product/<int:product_id>`
- **Methods**: `GET`
- **Purpose**: Decreases the stock of a product by one and confirms the purchase.

### 5. User Logout
- **Endpoint**: `/user_logout`
- **Purpose**: Logs out the user and redirects to the login page.

### 6. Add to Cart
- **Endpoint**: `/add-to-cart/<int:product_id>`
- **Methods**: `POST`
- **Purpose**: Adds a product to the user's cart or increments its quantity if already present.

### 7. Remove from Cart
- **Endpoint**: `/remove-from-cart/<int:item_id>`
- **Methods**: `GET`
- **Purpose**: Removes a product from the user's cart.

### 8. Orders
- **Endpoint**: `/checkout`
- **Methods**: `GET`, `POST`
- **Purpose**: Displays the user's cart for checkout. On confirmation, updates product stocks and clears the cart.

### 9. Add Review for Feedback
- **Endpoint**: `/add_review/<int:product_id>`
- **Methods**: `POST`
- **Purpose**: Allows users to add a review for a product Feedback.

