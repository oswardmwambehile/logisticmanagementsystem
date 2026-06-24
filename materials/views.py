from django.shortcuts import render, redirect, get_object_or_404
from .models import MaterialCategory
from .forms import MaterialCategoryForm
from django.contrib import messages


def category_view(request):

    categories = MaterialCategory.objects.all()
    form = MaterialCategoryForm()

    # ================= CREATE =================
    if request.method == "POST" and "create_category" in request.POST:

        form = MaterialCategoryForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully")
            return redirect('category_view')

    # ================= UPDATE =================
    if request.method == "POST" and "update_category" in request.POST:

        category = get_object_or_404(MaterialCategory, id=request.POST.get('category_id'))

        form = MaterialCategoryForm(request.POST, instance=category)

        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully")
            return redirect('category_view')

    # ================= DELETE =================
    if request.method == "POST" and "delete_category" in request.POST:

        category = get_object_or_404(MaterialCategory, id=request.POST.get('category_id'))
        category.delete()

        messages.success(request, "Category deleted successfully")
        return redirect('category_view')

    return render(request, "manager/category_view.html", {
        "categories": categories,
        "form": form
    })


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import MaterialForm


def material_create_view(request):

    if request.method == "POST":
        form = MaterialForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            messages.success(request, "Material created successfully!")
            return redirect('material_list')  # change later

        else:
            messages.error(request, "Please fix the errors below.")

    else:
        form = MaterialForm()

    return render(request, "manager/material_form.html", {
        "form": form
    })

from django.shortcuts import render
from .models import Material


def material_list_view(request):

    materials = Material.objects.select_related('category').all()

    return render(request, "manager/material_list.html", {
        "materials": materials
    })


from django.shortcuts import render, get_object_or_404
from .models import Material


def material_detail_view(request, pk):
    material = get_object_or_404(Material, pk=pk)

    # stock history (optional but useful)
    movements = material.movements.all().order_by('-created_at')

    return render(request, "manager/material_detail.html", {
        "material": material,
        "movements": movements
    })

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Material


def material_delete_view(request, pk):

    material = get_object_or_404(Material, pk=pk)

    if request.method == "POST":
        material.delete()

        return JsonResponse({
            "success": True,
            "message": "Material deleted successfully"
        })

    return JsonResponse({
        "success": False,
        "message": "Invalid request"
    }, status=400)



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Material
from .forms import MaterialForm


def material_update_view(request, pk):

    material = get_object_or_404(Material, pk=pk)

    if request.method == "POST":

        form = MaterialForm(
            request.POST,
            request.FILES,
            instance=material
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Material updated successfully")
            return redirect('material_list')

        else:
            messages.error(request, "Please correct the errors below")

    else:
        form = MaterialForm(instance=material)

    return render(request, "manager/material_form.html", {
        "form": form,
        "material": material
    })


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StockMovementForm
from .models import StockMovement


def stock_movement_list_create(request):

    movements = StockMovement.objects.select_related('material').order_by('-created_at')

    if request.method == "POST":
        form = StockMovementForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Stock movement recorded successfully")
            return redirect('stock_movement_list')

        messages.error(request, "Please fix the errors below")

    else:
        form = StockMovementForm()

    return render(request, "manager/stock_movement.html", {
        "form": form,
        "movements": movements
    })


from django.db.models import Q
from .models import Material, MaterialCategory

def customer_material_list_view(request):
    category_id = request.GET.get('category')
    search = request.GET.get('search')

    materials = Material.objects.all()
    categories = MaterialCategory.objects.all()

    if category_id:
        materials = materials.filter(category_id=category_id)

    if search:
        materials = materials.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(category__name__icontains=search)
        )

    context = {
        "materials": materials,
        "categories": categories,
        "selected_category": category_id,
        "search": search,
    }

    return render(request, "customers/material_list.html", context)


# views.py

from django.shortcuts import render, get_object_or_404
from .models import Material

def customer_material_detail_view(request, pk):
    material = get_object_or_404(Material, pk=pk)

    context = {
        "material": material,
    }

    return render(
        request,
        "customers/material_detail.html",
        context,
    )