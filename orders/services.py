from django.db import transaction
from accounts.models import User
from orders.models import Order


def assign_driver_to_order(order):

    with transaction.atomic():

        # LOCK AVAILABLE DRIVERS
        driver = User.objects.select_for_update().filter(
            role="DRIVER",
            is_available=True
        ).order_by("id").first()

        if not driver:
            order.status = "PENDING"
            order.driver = None
            order.save()
            return None

        # IMPORTANT: prevent double assignment
        if order.driver is not None:
            return order.driver

        # assign driver
        order.driver = driver
        order.status = "ASSIGNED"
        order.save()

        # mark driver busy
        driver.is_available = False
        driver.save()

        return driver
    

def dispatch_system():

    with transaction.atomic():

        pending_orders = Order.objects.filter(
            status="PENDING",
            driver__isnull=True
        ).order_by("created_at")

        for order in pending_orders:

            # stop if no drivers
            driver = User.objects.select_for_update().filter(
                role="DRIVER",
                is_available=True
            ).order_by("id").first()

            if not driver:
                break

            # prevent double assignment
            if order.driver:
                continue

            order.driver = driver
            order.status = "ASSIGNED"
            order.save()

            driver.is_available = False
            driver.save()