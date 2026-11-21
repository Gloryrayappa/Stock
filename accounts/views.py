from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect


def accounts(request):
    return render(request, "accounts/accounts.html", {"active": "accounts"})


def signup(request):
    if request.user.is_authenticated:
        return redirect("inventory-dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not username or not email or not password:
            messages.error(request, "Username, email, and password are required.")
        elif User.objects.filter(username__iexact=username).exists():
            messages.error(request, "This username is already in use.")
        elif User.objects.filter(email__iexact=email).exists():
            messages.error(request, "This email is already registered.")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")
        elif len(password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
            login(request, user)
            messages.success(request, f"Welcome, {username}! Your account has been created.")
            return redirect("inventory-dashboard")

    return render(request, "accounts/signup.html", {"active": "accounts"})
