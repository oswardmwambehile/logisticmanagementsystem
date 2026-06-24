from django.shortcuts import render
from django.shortcuts import render

def home(request):
    return render(request, 'customers/index.html')



from django.shortcuts import render
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from orders.models import Order


def driver_dashboard(request):

    driver = request.user

    # DRIVER ORDERS ONLY
    orders = Order.objects.filter(driver=driver)

    assigned_orders = orders.filter(status='ASSIGNED')
    on_route_orders = orders.filter(status='ON_ROUTE')
    delivered_orders = orders.filter(status='DELIVERED')

    # TOTAL COUNTS
    total_assigned = assigned_orders.count()
    total_on_route = on_route_orders.count()
    total_delivered = delivered_orders.count()

    # REVENUE FROM DELIVERED ORDERS
    revenue = delivered_orders.annotate(
        total=ExpressionWrapper(
            F('items__quantity') * F('items__unit_price'),
            output_field=DecimalField()
        )
    ).aggregate(total_revenue=Sum('total'))['total_revenue'] or 0

    return render(request, 'driver/driver_dashboard.html', {
        "assigned_orders": total_assigned,
        "on_route_orders": total_on_route,
        "delivered_orders": total_delivered,
        "revenue": revenue,

        "assigned_list": assigned_orders,
        "on_route_list": on_route_orders,
        "delivered_list": delivered_orders,
    })


from django.shortcuts import render
from orders.models import Order


def driver_profile(request):

    driver = request.user

    # DRIVER ORDERS
    orders = Order.objects.filter(driver=driver)

    total_orders = orders.count()
    delivered = orders.filter(status='DELIVERED').count()
    on_route = orders.filter(status='ON_ROUTE').count()
    assigned = orders.filter(status='ASSIGNED').count()

    return render(request, 'driver/profile.html', {
        "driver": driver,
        "total_orders": total_orders,
        "delivered": delivered,
        "on_route": on_route,
        "assigned": assigned,
    })


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login,logout
from .forms import RegisterForm

def register_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Account created successfully. Please login."
            )

            return redirect('login')

        messages.error(
            request,
            "Please correct the errors below."
        )

    else:
        form = RegisterForm()

    return render(
        request,
        "customers/register.html",
        {"form": form}
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

from django.contrib import messages
from django.shortcuts import render, redirect

from accounts.forms import DriverCreateForm
from orders.services import dispatch_system


def driver_create(request):

    if request.method == "POST":
        form = DriverCreateForm(request.POST)

        if form.is_valid():

            driver = form.save()

            # ⭐ IMPORTANT: run dispatch engine after driver is created
            dispatch_system()

            messages.success(
                request,
                "Driver created successfully and orders assigned if available."
            )

            return redirect("driver_list")

    else:
        form = DriverCreateForm()

    return render(
        request,
        "manager/driver_form.html",
        {
            "form": form
        }
    )
from django.shortcuts import render
from accounts.models import User


def driver_list(request):

    drivers = User.objects.filter(
        role="DRIVER"
    ).order_by("-created_at")

    return render(
        request,
        "manager/driver_list.html",
        {
            "drivers": drivers
        }
    )

from django.shortcuts import render, get_object_or_404
from accounts.models import User


def driver_detail(request, pk):

    driver = get_object_or_404(
        User,
        id=pk,
        role="DRIVER"
    )

    return render(
        request,
        "manager/driver_detail.html",
        {
            "driver": driver
        }
    )



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from accounts.models import User
from accounts.forms import DriverUpdateForm


def driver_update(request, pk):

    driver = get_object_or_404(
        User,
        id=pk,
        role="DRIVER"
    )

    if request.method == "POST":

        form = DriverUpdateForm(
            request.POST,
            instance=driver
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Driver updated successfully."
            )

            return redirect(
                "driver_detail",
                pk=driver.id
            )

    else:

        form = DriverUpdateForm(
            instance=driver
        )

    return render(
        request,
        "manager/driver_form.html",
        {
            "form": form,
            "driver": driver,
            "is_update": True,
        }
    )



from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from accounts.models import User


def driver_delete(request, pk):

    driver = get_object_or_404(
        User,
        id=pk,
        role="DRIVER"
    )

    # Only allow POST for safety
    if request.method == "POST":

        driver.delete()

        return JsonResponse({
            "success": True,
            "message": "Driver deleted successfully"
        })

    return JsonResponse({
        "success": False,
        "message": "Invalid request"
    })


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

from .forms import PasswordChangeFormCustom


def change_password(request):

    if request.method == "POST":

        form = PasswordChangeFormCustom(request.POST)

        if form.is_valid():

            user = request.user

            old_password = form.cleaned_data["old_password"]
            new_password = form.cleaned_data["new_password"]

            # CHECK OLD PASSWORD
            if not user.check_password(old_password):
                messages.error(request, "Old password is incorrect")
                return redirect("change_password")

            # SET NEW PASSWORD
            user.set_password(new_password)
            user.save()

            update_session_auth_hash(request, user)

            messages.success(request, "Password changed successfully")

            return redirect("change_password")

    else:
        form = PasswordChangeFormCustom()

    return render(request, "driver/change_password.html", {
        "form": form
    })



def customer_change_password(request):

    if request.method == "POST":

        form = PasswordChangeFormCustom(request.POST)

        if form.is_valid():

            user = request.user

            old_password = form.cleaned_data["old_password"]
            new_password = form.cleaned_data["new_password"]

            # CHECK OLD PASSWORD
            if not user.check_password(old_password):
                messages.error(request, "Old password is incorrect")
                return redirect("change_password")

            # SET NEW PASSWORD
            user.set_password(new_password)
            user.save()

            update_session_auth_hash(request, user)

            messages.success(request, "Password changed successfully")

            return redirect("change_password")

    else:
        form = PasswordChangeFormCustom()

    return render(request, "customers/change_password.html", {
        "form": form
    })