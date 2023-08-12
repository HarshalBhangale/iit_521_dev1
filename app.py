from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, current_user, login_required, login_user, logout_user, UserMixin
import matplotlib.pyplot as plt
import numpy as np
import base64
from io import BytesIO


app = Flask(__name__)

# Configuations
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#######################################################################
##### DATABASE MODELS ##### DATABASE MODELS ##### DATABASE MODELS ##### 
#######################################################################

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    cart_items = db.relationship('CartItem', back_populates='user')

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    price_per_unit = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    cart_items = db.relationship('CartItem', back_populates='product')

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', back_populates='cart_items')
    product = db.relationship('Product', back_populates='cart_items')
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    cart = db.relationship('Cart', back_populates='cart_items', foreign_keys=[cart_id])
    def calculate_total_price(self):
        return self.product.price_per_unit * self.quantity
        

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cart_items = db.relationship('CartItem', back_populates='cart')
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    content = db.Column(db.String(500), nullable=False)

##########################################################################
##### Routes #####  Routes #####  Routes #####  Routes #####  Routes ##### 
##########################################################################
    
''' ********************************************************************************'''
''' ********************************************************************************'''

#########################################################################
##### MANAGER ROUTES #####  MANAGER ROUTES #####  MANAGER ROUTES ##### ###
#########################################################################


@login_manager.user_loader
def load_user(user_id):
    # Assuming you have a User model that stores your user details
    return User.query.get(int(user_id))

# Routes for Manager Login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Hardcoded manager credentials
        if username == "manager" and password == "password":
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check your username and/or password.', 'danger')

    return render_template('index.html')
''' ********************************************************************************'''
# Manager Dashboard routes
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'logged_in' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('login'))

    categories = Category.query.all()
    return render_template('dashboard.html', categories=categories)
''' ********************************************************************************'''
# ROutes for category ie. Category Addition , editing and deletion
@app.route('/add-category', methods=['POST'])
def add_category():
    category_name = request.form.get('category_name')
    category = Category(name=category_name)
    db.session.add(category)
    db.session.commit()
    flash('Category added successfully!', 'success')
    return redirect(url_for('dashboard'))
''' ********************************************************************************'''
@app.route('/delete-category/<int:category_id>')
def delete_category(category_id):
    category = Category.query.get(category_id)
    if category:
        db.session.delete(category)
        db.session.commit()
        flash('Category deleted!', 'success')
    else:
        flash('Category not found!', 'danger')
    return redirect(url_for('dashboard'))
''' ********************************************************************************'''
@app.route('/edit-category/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        flash('Category not found!', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        category.name = request.form.get('category_name')
        db.session.commit()
        flash('Category updated!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_category.html', category=category)
''' ********************************************************************************'''
# ROutes for Products ie. Product Addition , editing and deletion
@app.route('/add-product/<int:category_id>', methods=['POST'])
def add_product(category_id):
    product_name = request.form.get('product_name')
    unit = request.form.get('unit')
    price_per_unit = request.form.get('price_per_unit')
    stock_quantity = request.form.get('stock_quantity')
    product = Product(name=product_name, unit=unit, price_per_unit=price_per_unit, stock_quantity=stock_quantity, category_id=category_id)
    db.session.add(product)
    db.session.commit()
    flash('Product added successfully!', 'success')
    return redirect(url_for('dashboard'))
''' ********************************************************************************'''
@app.route('/edit-product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        flash('Product not found!', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        product.name = request.form.get('product_name')
        product.unit = request.form.get('unit')
        product.price_per_unit = request.form.get('price_per_unit')
        product.stock_quantity = request.form.get('stock_quantity')
        db.session.commit()
        flash('Product updated!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_product.html', product=product)
''' ********************************************************************************'''
@app.route('/delete-product/<int:product_id>')
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted!', 'success')
    else:
        flash('Product not found!', 'danger')
    return redirect(url_for('dashboard'))
''' ********************************************************************************'''
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))
''' ********************************************************************************'''
@app.route('/summary')
def summary():
    # Generating Dummy Data
    total_orders = 1500
    total_sales = 25000
    out_of_order_items = 25
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    sales_per_day = [3000, 3200, 3400, 2900, 2800, 3500, 3600]
    favorite_product = "Parle Biscuits"
    weeks = ["Week 1", "Week 2", "Week 3", "Week 4"]
    sales_per_week = [3000, 3200, 3400, 2900]

    # Matplotlib: Total Sales for 7 days (Bar Chart)
    plt.figure(figsize=(10, 5))
    plt.bar(days, sales_per_day, color='blue')
    plt.xlabel('Day')
    plt.ylabel('Sales (In INR)')
    plt.title('Total Sales for the Last 7 Days')
    img = BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    sales_graph = base64.b64encode(img.getvalue()).decode()
    
    # Matplotlib: Total Sales for last month (Bar Chart)
    plt.figure(figsize=(10, 5))
    plt.bar(weeks, sales_per_week, color='green')
    plt.xlabel('Week of the Month')
    plt.ylabel('Sales (In thousands rupees)')
    plt.title('Total Sales for the Last Month')
    img = BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    sales_graph_2 = base64.b64encode(img.getvalue()).decode()

    # Matplotlib: Product Sales Distribution (Pie Chart)
    products = ['Mangos', 'apples', 'guava', 'bananas']
    products_sales = [12000, 8000, 7000, 9000]
    plt.figure(figsize=(10, 5))
    colors = ['red', 'green', 'blue', 'yellow']
    plt.pie(products_sales, labels=products, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title('Product Sales Distribution Pie Chart')
    img1 = BytesIO()
    plt.savefig(img1, format="png")
    img1.seek(0)
    products_sales_distribution_graph = base64.b64encode(img1.getvalue()).decode()

    # Matplotlib: User Activity for 7 days
    user_activity = [1000, 1200, 1100, 1050, 980, 1150, 1250]
    plt.figure(figsize=(10, 5))
    plt.plot(days, user_activity, marker='o', linestyle='-', color='purple')
    plt.xlabel('Day')
    plt.ylabel('Active Users')
    plt.title('User Activity Over the Last 7 Days')
    img2 = BytesIO()
    plt.savefig(img2, format="png")
    img2.seek(0)
    user_activity_graph = base64.b64encode(img2.getvalue()).decode()

    return render_template('summary.html', total_orders=total_orders, total_sales=total_sales,
                        out_of_order_items=out_of_order_items, favorite_product=favorite_product,
                        sales_graph=sales_graph, products_sales_distribution_graph=products_sales_distribution_graph,sales_graph_2 = sales_graph_2,
                        user_activity_graph=user_activity_graph)

#########################################################################
######  User ROUTES ##### User ROUTES ##### User ROUTES ##### User ROUTES ##### 
#########################################################################
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user_login'
''' ********************************************************************************'''
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
''' ********************************************************************************'''
@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if current_user.is_authenticated:
        return redirect(url_for('user_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid username or password', 'danger')   
    return render_template('user_login.html')
''' ********************************************************************************'''
@app.route('/user_register', methods=['GET', 'POST'])
def user_register():
    if current_user.is_authenticated:
        return redirect(url_for('user_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('user_login'))
    
    return render_template('user_register.html')
''' ********************************************************************************'''
# User Dashboard routes
@app.route('/user_dashboard', methods=['GET'])
@login_required
def user_dashboard():
    categories = Category.query.all()
    products = Product.query.all()
    search_query = request.args.get('search_query', '')
    sort_option = request.args.get('sort_option', '')
    print(search_query, sort_option)
    if search_query:
        products = Product.query.filter(Product.name.ilike(f'%{search_query}%'))
        print(products)
    if sort_option == 'name_asc':
        products = sorted(products, key=lambda x: x.name)
        
    elif sort_option == 'name_desc':
        products = sorted(products, key=lambda x: x.name, reverse=True)
    elif sort_option == 'price_asc':
        products = sorted(products, key=lambda x: x.price_per_unit)
    elif sort_option == 'price_desc':
        products = sorted(products, key=lambda x: x.price_per_unit, reverse=True)

    cart_items = CartItem.query.join(Cart).filter(Cart.user_id == current_user.id).all()
    cart_total = sum(item.calculate_total_price() for item in cart_items)
    return render_template('user_dashboard.html', categories=categories, products=products, cart_items=cart_items, cart_total=cart_total)
''' ********************************************************************************'''
# Routes for Buying products
@app.route('/buy-product/<int:product_id>', methods=['GET'])
def buy_product(product_id):
    product = Product.query.get(product_id)
    if product and product.stock_quantity > 0:
        product.stock_quantity -= 1
        db.session.commit()
        flash('Product purchased successfully!', 'success')
    else:
        flash('Product not available or out of stock.', 'danger')
    return redirect(url_for('user_dashboard'))
''' ********************************************************************************'''
# Routes for user logout
@app.route('/user_logout')
@login_required
def user_logout():
    logout_user()
    return redirect(url_for('user_login'))
''' ********************************************************************************'''
# Routes for USer adding items to cart
@app.route('/add-to-cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    user_id = current_user.id
    product = Product.query.get(product_id)
    if not product:
        flash('Product not found!', 'danger')
        return redirect(url_for('user_dashboard'))
    # Check if the user has a cart, and create one if not
    user_cart = Cart.query.filter_by(user_id=user_id).first()
    if not user_cart:
        user_cart = Cart(user_id=user_id)
        db.session.add(user_cart)
    # Check if the product is already in the user's cart
    existing_item = CartItem.query.filter_by(user_id=user_id, product_id=product_id, cart_id=user_cart.id).first()
    if existing_item:
        existing_item.quantity += 1
    else:
        new_item = CartItem(user_id=user_id, product_id=product_id, quantity=1, cart_id=user_cart.id)
        db.session.add(new_item)
    db.session.commit()
    flash('Product added to cart!', 'success')
    return redirect(url_for('user_dashboard'))
''' ********************************************************************************'''
# For removing a product from Cart
@app.route('/remove-from-cart/<int:item_id>', methods=['GET'])
@login_required
def remove_from_cart(item_id):
    item = CartItem.query.get(item_id)

    if item:
        db.session.delete(item)
        db.session.commit()
        flash('Item removed from cart!', 'success')
    else:
        flash('Item not found in cart.', 'danger')

    return redirect(url_for('user_dashboard'))
''' ********************************************************************************'''
# Orders page 
@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    user_id = current_user.id
    cart_items = CartItem.query.filter_by(user_id=user_id).all()

    if request.method == 'POST':
        # Implement your checkout logic here
        # Update product quantities, calculate total, etc.
        # Once checkout is complete, remove items from cart

        for item in cart_items:
            product = Product.query.get(item.product_id)
            if product:
                product.stock_quantity -= item.quantity
                db.session.delete(item)

        db.session.commit()
        return redirect(url_for('user_dashboard'))

    return render_template('checkout.html', cart_items=cart_items)
''' ********************************************************************************'''
# calculating total amount in Cart
def calculate_total_amount(cart_items):
    total_amount = 0
    for item in cart_items:
        total_amount += item.product.price_per_unit * item.quantity
    return total_amount
''' ********************************************************************************'''
@app.route('/add_review/<int:product_id>', methods=['POST'])
@login_required
def add_review(product_id):
    content = request.form.get('review_content')
    review = Review(user_id=current_user.id, product_id=product_id, content=content)
    db.session.add(review)
    db.session.commit()
    return redirect(url_for('checkout'))
''' ********************************************************************************'''

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

''' ********************************************************************************'''
### END OF MAD1 Project ### END OF MAD1 Project ### END OF MAD1 Project ### END OF MAD1 Project ###
### END OF MAD1 Project ### END OF MAD1 Project ### END OF MAD1 Project ### END OF MAD1 Project ###