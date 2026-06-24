from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction

from materials.models import Material
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemForm


from django.db import transaction
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from materials.models import Material
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemForm

from orders.services import dispatch_system


@login_required
def customer_create_order(request, material_id):

    material = get_object_or_404(Material, id=material_id)

    if request.method == "POST":

        order_form = OrderForm(request.POST)
        item_form = OrderItemForm(request.POST)

        if order_form.is_valid() and item_form.is_valid():

            quantity = item_form.cleaned_data['quantity']

            # STOCK VALIDATION
            if quantity > material.stock_quantity:

                item_form.add_error(
                    'quantity',
                    f"Only {material.stock_quantity} available in stock. You cannot place order above stock."
                )

            else:

                with transaction.atomic():

                    # CREATE ORDER
                    order = order_form.save(commit=False)
                    order.customer = request.user
                    order.status = "PENDING"
                    order.save()

                    # CREATE ORDER ITEM
                    OrderItem.objects.create(
                        order=order,
                        material=material,
                        quantity=quantity,
                        unit_price=material.price
                    )

                    # REDUCE STOCK
                    material.stock_quantity -= quantity
                    material.save()

                # ⭐ RUN DISPATCH AFTER COMMIT
                dispatch_system()

                return redirect("order_success", order_id=order.id)

    else:
        order_form = OrderForm()
        item_form = OrderItemForm()

    return render(request, "customers/customer_create_order.html", {
        "material": material,
        "order_form": order_form,
        "item_form": item_form,
    })
from django.shortcuts import render, get_object_or_404
from .models import Order


def order_success_view(request, order_id):
    order = get_object_or_404(
        Order.objects.select_related("customer").prefetch_related("items__material"),
        id=order_id,
        customer=request.user
    )

    return render(request, "customers/order_success.html", {
        "order": order
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Order


@login_required
def customer_orders(request):

    orders = (
        Order.objects
        .filter(customer=request.user)
        .select_related("driver")
        .prefetch_related("items__material")
        .order_by("-created_at")
    )

    for order in orders:
        order.total = sum(
            item.quantity * item.unit_price
            for item in order.items.all()
        )

    return render(
        request,
        "customers/customer_orders.html",
        {
            "orders": orders
        }
    )


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Order


@login_required
def driver_assigned_orders(request):

    orders = Order.objects.filter(
        driver=request.user,
        status='ASSIGNED'   # ONLY assigned
    ).order_by('-created_at')

    return render(request, 'driver/assigned_orders.html', {
        'orders': orders
    })


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .models import Order



from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from orders.models import Order


@login_required
def driver_order_detail(request, pk):

    order = get_object_or_404(Order, pk=pk)

    # allow only assigned driver
    if order.driver != request.user:
        return HttpResponseForbidden("You are not assigned to this order")

    return render(request, 'driver/order_detail.html', {
        'order': order
    })



from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from orders.models import Order
from .services import dispatch_system


@login_required
def update_order_status(request, pk, status):

    order = get_object_or_404(Order, pk=pk)

    # 🔒 ONLY ASSIGNED DRIVER CAN UPDATE
    if order.driver != request.user:
        return HttpResponseForbidden("Not your order")

    # =========================
    # MOVE TO ON ROUTE
    # =========================
    if status == "ON_ROUTE" and order.status == "ASSIGNED":
        order.status = "ON_ROUTE"
        order.save()

    # =========================
    # DELIVERY COMPLETED
    # =========================
    elif status == "DELIVERED" and order.status == "ON_ROUTE":

        order.status = "DELIVERED"
        order.save()

        # STEP 1: free driver
        driver = order.driver
        if driver:
            driver.is_available = True
            driver.save()

        # ❌ DO NOT REMOVE DRIVER (IMPORTANT FIX)
        # order.driver = None

        # STEP 2: auto assign next orders
        dispatch_system()

    return redirect('driver_order_detail', pk=order.id)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from orders.models import Order


@login_required
def driver_on_route_orders(request):

    orders = Order.objects.filter(
        driver=request.user,
        status="ON_ROUTE"
    ).order_by("-created_at")

    return render(request, "driver/assigned_orders.html", {
        "orders": orders
    })


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from orders.models import Order


@login_required
def driver_delivered_orders(request):

    orders = Order.objects.filter(
        driver=request.user,
        status="DELIVERED"
    ).order_by("-created_at")

    return render(request, "driver/assigned_orders.html", {
        "orders": orders
    })




from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from orders.models import Order



def admin_pending_orders(request):
    orders = Order.objects.filter(status="PENDING").order_by("-created_at")
    return render(request, "manager/assigned_orders.html", {
        "orders": orders,
        "title": "Pending Orders"
    })



def admin_assigned_orders(request):
    orders = Order.objects.filter(status="ASSIGNED").order_by("-created_at")
    return render(request, "manager/assigned_orders.html", {
        "orders": orders,
        "title": "Assigned Orders"
    })



def admin_on_route_orders(request):
    orders = Order.objects.filter(status="ON_ROUTE").order_by("-created_at")
    return render(request, "manager/assigned_orders.html", {
        "orders": orders,
        "title": "On Route Orders"
    })



def admin_delivered_orders(request):
    orders = Order.objects.filter(status="DELIVERED").order_by("-created_at")
    return render(request, "manager/assigned_orders.html", {
        "orders": orders,
        "title": "Delivered Orders"
    })


# views.py
from django.shortcuts import render, get_object_or_404
from .models import Order


def admin_order_detail(request, pk):
    order = get_object_or_404(
        Order.objects.prefetch_related('items__material', 'customer', 'driver'),
        pk=pk
    )

    total = sum(item.quantity * item.unit_price for item in order.items.all())

    return render(request, "manager/admin_order_detail.html", {
        "order": order,
        "total": total
    })

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from orders.models import Order


@login_required
def order_delete(request, pk):

    if request.user.role != "ADMIN":
        messages.error(request, "Permission denied.")
        return redirect("dashboard")

    order = get_object_or_404(Order, pk=pk)

    order.delete()

    

    return redirect("admin_delivered_orders")