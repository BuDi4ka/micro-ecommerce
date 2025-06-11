from django.shortcuts import render, redirect

# Create your views here.
from .models import Product
from .forms import ProductForm


def product_create(request):
    context = {}
    form = ProductForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        if request.user.is_authenticated:
            obj.user = request.user
            obj.save()
            return redirect('products:create')
        form.add_error(None, "You must be logged in to create products")

    context["form"] = form
    return render(request, "products/create.html", context)


def product_list(request):
    return render(request, "products/list.html", {})
