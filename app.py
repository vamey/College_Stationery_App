from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session

app = Flask(__name__)

# Sample data: stationery items
products = {
    1: {"name": "Notebook", "price": 50, "quantity": 100},
    2: {"name": "Pen", "price": 10, "quantity": 200},
    3: {"name": "Eraser", "price": 5, "quantity": 150},
}

cart = []  # Store user's cart items

@app.route('/')
def home():
    """Display available stationery products."""
    return render_template('home.html', products=products)


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    """Add or subtract quantities of selected products in the cart."""
    for product_id, product in products.items():
        # Get the new quantity input for each product
        new_quantity = int(request.form.get(f'quantity_{product_id}', 0))
        if new_quantity >= 0:  # Ensure valid input
            found = False
            for item in cart:
                if item['product']['name'] == product['name']:
                    # Calculate the difference between new and current quantity
                    quantity_difference = new_quantity - item['quantity']

                    if quantity_difference > 0:  # User adds more items
                        if product["quantity"] >= quantity_difference:
                            item['quantity'] = new_quantity  # Update quantity in cart
                            product["quantity"] -= quantity_difference  # Subtract stock
                        else:
                            return f"Not enough stock for {product['name']}!"

                    elif quantity_difference < 0:  # User reduces quantity
                        product["quantity"] += abs(quantity_difference)  # Add back stock
                        item['quantity'] = new_quantity  # Update quantity in cart

                    # If quantity becomes zero, remove item from the cart
                    if item['quantity'] == 0:
                        cart.remove(item)
                    found = True
                    break

            # If product not found in cart, add it if quantity > 0
            if not found and new_quantity > 0:
                if product["quantity"] >= new_quantity:
                    cart.append({"product": product, "quantity": new_quantity})
                    product["quantity"] -= new_quantity
                else:
                    return f"Not enough stock for {product['name']}!"

    return redirect(url_for('view_cart'))



@app.route('/cart')
def view_cart():
    """Display cart items."""
    total_price = sum(item['product']['price'] * item['quantity'] for item in cart)
    return render_template('cart.html', cart=cart, total_price=total_price)

@app.route('/checkout', methods=['POST'])
def checkout():
    payment_method = request.form['payment_method']
    if payment_method == 'Online':
        return render_template('online_payment.html')  # New page for online payment
    elif payment_method == 'Cash on Collection':
        return render_template('order_confirmation.html', payment_method=payment_method)
    return "Invalid payment method!"



if __name__ == '__main__':
    app.run(debug=True)
