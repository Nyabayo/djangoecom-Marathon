from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Product  # Import the Product model
from .forms import SignUpForm

# Home view
def home(request):
    products = Product.objects.all()  # Fetch products from the database
    return render(request, 'home.html', {'products': products})

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
