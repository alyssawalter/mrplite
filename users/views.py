from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password1)

        # Log the user in
        login(request, user)

        # Display success message
        messages.success(request, "Welcome to the MRP Lite dashboard. Feel free to explore!")

        # Redirect to dashboard or any other page
        return redirect('dashboard')
    else:
        return render(request, 'users/signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard after successful login
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'users/login.html')  # Render the login template


def logout_view(request):
    logout(request)
    return redirect('homepage')  # Redirect to the homepage after logout

