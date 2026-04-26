from flask import render_template, session, request, redirect, url_for
from app import app
from model.cart import Cart


def get_cart():
    cart_id = session.get('cart_id')
    if cart_id:
        cart = Cart.query.filter_by(id=cart_id, status=0).first()  # ✅ active cart only
        if cart:
            return cart

    # fallback: find active cart by user_id
    user_id = session.get('user_id')
    if user_id:
        return Cart.query.filter_by(user_id=user_id, status=0).first()  # ✅ filter by status

    return None


def get_total():
    cart = get_cart()

    if cart and cart.items:
        return sum(float(i.price) * i.quantity for i in cart.items)

    return 0


@app.route('/payment', methods=['GET', 'POST'])
def payment():

    cart = get_cart()

    if not cart or not cart.items:
        return redirect('/cart')

    items = cart.items or []
    total = sum(float(i.price) * i.quantity for i in items)

    if total <= 0:
        return redirect('/cart')

    if request.method == 'POST':

        customer_name = request.form.get("customer_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        address = request.form.get("address")

        if not all([customer_name, email, phone, address]):
            return render_template(
                'pageFront/payment.html',
                cart_total=total,
                cart=cart,
                error="Please fill all fields"
            )

        session['checkout'] = {
            "customer_name": customer_name,
            "email": email,
            "phone": phone,
            "address": address
        }

        return redirect(url_for('qr_payment'))

    return render_template(
        'pageFront/payment.html',
        cart_total=total,
        cart=cart
    )