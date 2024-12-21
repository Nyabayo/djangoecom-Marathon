from django.contrib.messages.api import success
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Product, Category  # Import the Product model, Category model
from .forms import SignUpForm

# Category pages view
def category(request, foo):
    foo = foo.replace('-', ' ')  # Grab the category from the URL
    try:
        # Look up the category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})
    except Category.DoesNotExist:
        messages.error(request, "Category doesn't exist")
        return redirect('home')

# Product view - individual product page
def product(request, pk):
    # Use get_object_or_404 to handle missing products gracefully
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product.html', {'product': product})

# Home view
def home(request):
    products = Product.objects.all()  # Fetch products from the database
    categories = Category.objects.all()  # Fetch all categories from the database
    return render(request, 'home.html', {'products': products, 'categories': categories})

# About view
def about(request):
    return render(request, 'about.html')

# Login view
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    return render(request, 'login.html')

# Logout view
def logout_user(request):
    logout(request)
    messages.success(request, 'You are now logged out.')
    return redirect('login')

# Registration view
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)  # Bind the form with POST data
        if form.is_valid():  # Validate the form
            form.save()  # Save the new user to the database
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            # Authenticate and log the user in
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You are now registered and logged in.')
                return redirect('home')  # Redirect to home page after successful registration
            else:
                messages.error(request, 'There was an issue logging you in after registration.')
                return redirect('login')  # Redirect to login page if something went wrong
        else:
            messages.error(request, 'There was a problem with the registration form. Please try again.')
            return render(request, 'register.html', {'form': form})  # Re-render the form with errors
    else:
        form = SignUpForm()  # Render an empty form if it's a GET request
        return render(request, 'register.html', {'form': form})
