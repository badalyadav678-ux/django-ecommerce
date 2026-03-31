from django.shortcuts import render, redirect
from .models import Product
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm


# 🏠 Home Page
from django.db.models import Q

def home(request):
    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        products = Product.objects.all()

    cart = request.session.get('cart', {})
    cart_count = len(cart)

    return render(request, 'home.html', {
        'products': products,
        'cart_count': cart_count
    })
# 📦 Product Detail Page
from django.shortcuts import get_object_or_404

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})


# 🛒 Add to Cart
@login_required
def add_to_cart(request, id):
    if request.method == 'POST':   # ✅ IMPORTANT

        cart = request.session.get('cart', {})

        if isinstance(cart, list):
            cart = {}

        id = str(id)

        if id in cart:
            cart[id] += 1
        else:
            cart[id] = 1

        request.session['cart'] = cart

        messages.success(request, "Item added to cart successfully!")

    return redirect('home')

# 🛍 Cart Page
@login_required
def cart_view(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0

    for id, qty in cart.items():
        product = Product.objects.get(id=id)
        total += product.price * qty

        products.append({
            'product': product,
            'quantity': qty
        })

    return render(request, 'cart.html', {
        'products': products,
        'total': total
    })


# ❌ Remove from Cart
def remove_from_cart(request, id):
    cart = request.session.get('cart', {})

    id = str(id)
    if id in cart:
        del cart[id]

    request.session['cart'] = cart
    return redirect('cart')


# ➕ Increase Quantity
def increase_quantity(request, id):
    cart = request.session.get('cart', {})

    id = str(id)
    if id in cart:
        cart[id] += 1

    request.session['cart'] = cart
    return redirect('cart')


# ➖ Decrease Quantity
def decrease_quantity(request, id):
    cart = request.session.get('cart', {})

    id = str(id)
    if id in cart:
        cart[id] -= 1
        if cart[id] <= 0:
            del cart[id]

    request.session['cart'] = cart
    return redirect('cart')


# 🔐 Signup
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})


# 🔐 Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html')


# 🔓 Logout
def user_logout(request):
    request.session.flush()
    logout(request)
    return redirect('home')

from .models import Order, OrderItem

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0

    for id, qty in cart.items():
        product = get_object_or_404(Product, id=id)
        total += product.price * qty

        products.append({
            'product': product,
            'quantity': qty,
            'id': id
            })

    if request.method == 'POST':
        address = request.POST['address']

        # ✅ Create Order
        order = Order.objects.create(
            user=request.user,
            address=address,
            total_price=total
        )

        # ✅ Save each product in OrderItem
        for id, qty in cart.items():
            product = Product.objects.get(id=id)

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=qty
            )

        # Clear cart
        request.session['cart'] = {}

        return redirect('order_success')

    return render(request, 'checkout.html', {
        'products': products,
        'total': total
    })


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'my_orders.html', {
        'orders': orders
    })

def order_success(request):
    return render(request, 'order_success.html')