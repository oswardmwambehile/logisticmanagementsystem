from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum, Count, F, ExpressionWrapper, DecimalField

from orders.models import Order
from accounts.models import User
from materials.models import Material

# 👉 ADD THIS (chat model assumed)



def admin_dashboard(request):

    today = timezone.now().date()

    # =========================
    # ORDERS METRICS
    # =========================
    orders = Order.objects.all()

    total_orders = orders.count()
    pending_orders = orders.filter(status='PENDING').count()
    assigned_orders = orders.filter(status='ASSIGNED').count()
    on_route_orders = orders.filter(status='ON_ROUTE').count()
    delivered_orders = orders.filter(status='DELIVERED').count()

    today_orders = orders.filter(created_at__date=today).count()

    # =========================
    # REVENUE (FIXED PROPERLY)
    # =========================
    revenue = Order.objects.filter(status='DELIVERED').aggregate(
        total=Sum(
            ExpressionWrapper(
                F('items__quantity') * F('items__unit_price'),
                output_field=DecimalField()
            )
        )
    )['total'] or 0

    # =========================
    # USERS METRICS
    # =========================
    total_customers = User.objects.filter(role='CUSTOMER').count()
    total_drivers = User.objects.filter(role='DRIVER').count()
    active_drivers = User.objects.filter(role='DRIVER', is_available=True).count()

    # =========================
    # MATERIALS METRICS
    # =========================
    total_materials = Material.objects.count()
    low_stock_materials = Material.objects.filter(stock_quantity__lte=5).count()

    top_materials = Material.objects.annotate(
        total_used=Sum('movements__quantity')
    ).order_by('-total_used')[:5]

    # =========================
    # RECENT ORDERS
    # =========================
    recent_orders = Order.objects.select_related('customer', 'driver').order_by('-created_at')[:10]

   

    # =========================
    # CHART DATA (FOR DASHBOARD)
    # =========================

    status_labels = ["Pending", "Assigned", "On Route", "Delivered"]
    status_data = [
        pending_orders,
        assigned_orders,
        on_route_orders,
        delivered_orders
    ]

    context = {
        # orders
        "total_orders": total_orders,
        "today_orders": today_orders,
        "pending_orders": pending_orders,
        "assigned_orders": assigned_orders,
        "on_route_orders": on_route_orders,
        "delivered_orders": delivered_orders,

        # revenue
        "revenue": revenue,

        # users
        "total_customers": total_customers,
        "total_drivers": total_drivers,
        "active_drivers": active_drivers,

        # materials
        "total_materials": total_materials,
        "low_stock_materials": low_stock_materials,
        "top_materials": top_materials,

        # orders table
        "recent_orders": recent_orders,

        
        # charts
        "status_labels": status_labels,
        "status_data": status_data,
    }

    return render(request, "manager/admin_dashboard.html", context)


from django.shortcuts import render
from accounts.models import User


def admin_customer_list(request):

    # GET ALL CUSTOMERS
    customers = User.objects.filter(role='CUSTOMER').order_by('-created_at')

    # OPTIONAL: extra analytics (nice for dashboard)
    total_customers = customers.count()

    recent_customers = User.objects.filter(
        role='CUSTOMER'
    ).order_by('-created_at')[:5]

    return render(request, 'manager/customer_list.html', {
        'customers': customers,
        'total_customers': total_customers,
        'recent_customers': recent_customers,
    })


from django.shortcuts import render, get_object_or_404
from accounts.models import User
from orders.models import Order


def admin_customer_detail(request, pk):

    # GET CUSTOMER
    customer = get_object_or_404(User, pk=pk, role='CUSTOMER')

    # CUSTOMER ORDERS
    orders = Order.objects.filter(customer=customer).order_by('-created_at')

    total_orders = orders.count()

    delivered_orders = orders.filter(status='DELIVERED').count()
    pending_orders = orders.filter(status='PENDING').count()

    # TOTAL SPENT (revenue per customer)
    total_spent = 0
    for order in orders.filter(status='DELIVERED'):
        total_spent += sum(item.subtotal() for item in order.items.all())

    return render(request, 'manager/customer_detail.html', {
        'customer': customer,
        'orders': orders,
        'total_orders': total_orders,
        'delivered_orders': delivered_orders,
        'pending_orders': pending_orders,
        'total_spent': total_spent,
    })