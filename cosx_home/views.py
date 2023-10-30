from genericpath import exists
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Products, Cart, Wallet, Orders, Rating, Wishlist
from django.db.models import Q
import random
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, 'cosx_home/home.html')


def register(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                # username already exists
                messages.error(request, "username already exists")
                return render(request, 'cosx_home/register.html')
            elif User.objects.filter(email=email).exists():
                # email already exists
                messages.error(request, "email already exists")
                return render(request, 'cosx_home/register.html')

            user = User.objects.create_user(
                username=username, email=email, password=password1, first_name=fname, last_name=lname)
            user.save()

            wallet = Wallet(user=user)
            wallet.save()

            return redirect('login')
        else:
            messages.error(request, "both passwords should match!!")
    return render(request, 'cosx_home/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('cosx-home')

        messages.error(request, "invalid username/password")
        return redirect('login')

    return render(request, 'cosx_home/login.html')


def logout(request):
    auth.logout(request)

    return redirect("login")


def password(request):

    thepassword = ""

    characters = list('abcdefghijklmnopqrstuvwxyz')

    length = int(request.GET.get('length', 12))

    characters.extend(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))

    characters.extend(list('!@#$%^&*()_+=-'))

    characters.extend(list('1234567890'))

    for i in range(length):
        thepassword += random.choice(characters)

    return render(request, 'cosx_home/password.html', {'password': thepassword})


def products(request):
    all_products = Products.objects.all()

    p_categories = set([prod.p_category for prod in all_products])
    # print(p_categories)

    if request.method == 'POST':
        category = {}
        all_none = True
        max_price = request.POST.get('max-price')
        all_products = Products.objects.none()

        active_categories = []

        for c in p_categories:
            if request.POST.get(c) is not None:
                active_categories.append(c)
        if len(active_categories) == 0:
            active_categories = p_categories
        all_products = Products.objects.filter(
            (Q(p_category__in=active_categories)) & (Q(p_price__lte=max_price)))

        # print(f"category: {all_products[0].p_image}")
        for i in range(len(all_products)):
            all_products[i].p_image = str(all_products[i].p_image)[
                len("/static/")-1:]
            all_products[i].p_name = (str(all_products[i].p_name)[:40] + '..') if len(
                str(all_products[i].p_name)) > 40 else str(all_products[i].p_name)
        context = {
            'products': all_products,
            'categories': p_categories
        }

        return render(request, 'cosx_home/products.html', context)

    query = request.GET.get('product', '')

    if query != '':
        all_products = Products.objects.filter(p_category__icontains=query).union(Products.objects.filter(
            p_name__icontains=query)).union(Products.objects.filter(p_description__icontains=query))

    for i in range(len(all_products)):
        all_products[i].p_buycount = len(
            Orders.objects.filter(product=all_products[i]))
        all_products[i].save()
        all_products[i].p_image = str(all_products[i].p_image)[
            len("/static/")-1:]
        all_products[i].p_name = (str(all_products[i].p_name)[:40] + '..') if len(
            str(all_products[i].p_name)) > 40 else str(all_products[i].p_name)

    context = {
        'products': all_products,
        'categories': p_categories
    }
    return render(request, 'cosx_home/products.html', context)


def productdetails(request, pk):
    product = Products.objects.get(id=pk)
    context = {
        'product': product,
    }
    return render(request, 'cosx_home/productdetails.html', context)


@login_required(login_url="/login/")
def cart(request):
    product_ids = Cart.objects.filter(user=request.user.id)

    if request.method == 'POST':
        p_id = request.POST.get('id')
        product = Products.objects.filter(id=p_id)[0]
        Cart.objects.filter(Q(product=product) & Q(user=request.user)).delete()

    if len(product_ids) == 0:
        return render(request, 'cosx_home/cart.html', context={})

    all_products = []
    for prod in product_ids:
        all_products.append(Products.objects.get(id=prod.product.id))

    return render(request, 'cosx_home/cart.html', context={'products': all_products, 'n_items': len(all_products)})


@login_required(login_url="/login/")
def cart_add(request, pk):

    if request.method == 'POST':
        p_id = request.POST.get('id')
        product = Products.objects.filter(id=p_id)[0]
        Cart.objects.filter(Q(product=product) & Q(user=request.user)).delete()

    product = Products.objects.get(id=pk)

    cart = Cart(user=request.user, product=product)
    for i in Cart.objects.all():
        if i.user.id == request.user.id and i.product.id == product.id:
            return redirect('/cart')
    cart.save()
    return redirect('/cart')


def checkout(request, pk):

    product = Products.objects.get(id=pk)
    total_price = product.p_price

    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        addr = request.POST.get('address')
        email = request.POST.get('email')
        phoneno = request.POST.get('phoneno')

        order = Orders(
            fname=fname,
            lname=lname,
            price=product.p_price,
            email=email,
            product=product,
            addr1=addr,
            phoneNum=phoneno,
            user=request.user
        )
        order.save()
        wallet = Wallet.objects.filter(user=request.user)[0]
        wallet.wallet -= total_price
        wallet.save()
        Cart.objects.filter(user=request.user).delete()

        return redirect('success')

    wallet = Wallet.objects.filter(user=request.user)[0].wallet
    flag = True
    if wallet < total_price:
        flag = False

    context = {
        'products': [product],
        'total_price': total_price,
        'flag': flag
    }
    return render(request, 'cosx_home/checkout.html', context=context)


def checkout_fromcart(request):

    products = []
    total_price = 0
    for i in Cart.objects.filter(user=request.user):
        if request.method == 'POST':
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            addr = request.POST.get('address')
            email = request.POST.get('email')
            phoneno = request.POST.get('phoneno')

            order = Orders(
                fname=fname,
                lname=lname,
                price=i.product.p_price,
                email=email,
                product=i.product,
                addr1=addr,
                phoneNum=phoneno,
                user=request.user
            )
            order.save()
        products.append(i.product)
        total_price += i.product.p_price

    if request.method == 'POST':
        wallet = Wallet.objects.filter(user=request.user)[0]
        if wallet.wallet >= total_price:
            wallet.wallet -= total_price
            wallet.save()
            Cart.objects.filter(user=request.user).delete()

            return redirect('success')

    wallet = Wallet.objects.filter(user=request.user)[0].wallet
    flag = True
    if wallet < total_price:
        flag = False

    context = {
        'products': products,
        'total_price': total_price,
        'flag': flag

    }

    return render(request, 'cosx_home/checkout.html', context=context)


def wallet(request):
    return render(request, 'cosx_home/wallet.html', context={'wallet':  Wallet.objects.filter(user=request.user)[0].wallet})


def success(request):
    return render(request, 'cosx_home/success.html')


def orders(request):

    all_orders = Orders.objects.filter(user=request.user)[::-1]

    context = {
        'orders': all_orders
    }
    if len(all_orders) == 0:
        context = {}
    return render(request, 'cosx_home/orders.html', context)


def order_details(request, pk):
    order = Orders.objects.filter(id=pk)[0]
    f = False
    rate_value = None
    if len(Rating.objects.filter(order=order)) == 0:
        f = True
    else:
        rate_value = Rating.objects.filter(order=order)[0].rating

    if request.method == 'POST':
        rating = request.POST.get('rating')
        rating = (int(rating)/20)
        if len(Rating.objects.filter(order=order)) == 0:
            rating_obj = Rating(order=order, rating=rating,
                                product=order.product)
            rating_obj.save()

            # calculating rating value when a new rating is added
            ratings = Rating.objects.filter(product=order.product)
            updated_rating = 0

            for i in ratings:
                updated_rating += i.rating

            updated_rating /= len(ratings)

            # updating rating value
            prod = Products.objects.filter(id=order.product.id)[0]
            prod.p_rating = updated_rating
            prod.save()

            f = False
        return render(request, 'cosx_home/order_details.html', context={'order': order, 'f': f, 'rating': rating})

    return render(request, 'cosx_home/order_details.html', context={'order': order, 'f': f, 'rating': rate_value})


def wishlist(request):
    product_ids = Wishlist.objects.filter(user=request.user.id)
    if len(product_ids) == 0:
        return render(request, 'cosx_home/wishlist.html', context={})

    all_products = []
    for prod in product_ids:
        all_products.append(Products.objects.get(id=prod.product.id))

    return render(request, 'cosx_home/wishlist.html', context={'products': all_products, 'n_items': len(all_products)})


def wishlist_add(request, pk):
    product = Products.objects.get(id=pk)
    wishlist = Wishlist(user=request.user, product=product)
    for i in Wishlist.objects.all():
        if i.user.id == request.user.id and i.product.id == product.id:
            return redirect('/wishlist')
    wishlist.save()
    return redirect('/wishlist')
