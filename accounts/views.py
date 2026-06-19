from django.shortcuts import render
from django.shortcuts import render

def home(request):
    return render(request, 'customers/index.html')



from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login,logout
from .forms import RegisterForm


def register_view(request):
    """
    Register a new customer account.
    """

    if request.user.is_authenticated:
        return redirect('home')  # Change to your home URL name

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # Force every registration to be a customer
            user.role = "customer"  # Remove if your model doesn't have role

            user.save()

            messages.success(
                request,
                "Account created successfully. Welcome!"
            )

            login(request, user)

            return redirect('home')  # Change to your desired page

        else:
            messages.error(
                request,
                "Please correct the errors below."
            )

    else:
        form = RegisterForm()

    context = {
        "form": form
    }

    return render(
        request,
        "customers/register.html",
        context
    )


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('home')
    else:
        messages.error(request,'You must login first to access the page')
        return redirect('login')


from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import LoginForm


def login_view(request):

    form = LoginForm(request, data=request.POST or None)

    if request.method == "POST":

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # ROLE REDIRECT LOGIC
            if user.role == "CUSTOMER":
                return redirect("home")

            elif user.role == "DRIVER":
                return redirect("driver_dashboard")

            elif user.role == "ADMIN":
                return redirect("admin_dashboard")

            # fallback
            return redirect("home")

        else:
            messages.error(request, "Invalid email or password")

    return render(request, "customers/login.html", {"form": form})