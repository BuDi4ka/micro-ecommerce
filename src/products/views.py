import mimetypes

from django.http import FileResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .models import Product, ProductAttachment
from .forms import ProductForm, ProductUpdateForm


def product_create(request):
    context = {}
    form = ProductForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        if request.user.is_authenticated:
            obj.user = request.user
            obj.save()
            return redirect("products:create")
        form.add_error(None, "You must be logged in to create products")

    context["form"] = form
    return render(request, "products/create.html", context)


def product_list(request):
    object_list = Product.objects.all()
    return render(request, "products/list.html", {"object_list": object_list})


def product_manage_detail(request, handle=None):
    obj = get_object_or_404(Product, handle=handle)
    is_manager = False
    if request.user.is_authenticated:
        is_manager = obj.user == request.user
    context = {"object": obj}
    print(context)
    if is_manager:
        form = ProductUpdateForm(
            request.POST or None, request.FILES or None, instance=obj
        )
        print(form)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            # return redirect("products:create")
        context["form"] = form
    return render(request, "products/detail.html", context)


def product_detail(request, handle=None):
    obj = get_object_or_404(Product, handle=handle)
    attachments = ProductAttachment.objects.filter(product=obj)
    is_owner = False
    if request.user.is_authenticated:
        is_owner = True
    context = {"object": obj, "is_owner": is_owner, "attachments": attachments}
    return render(request, "products/detail.html", context)


def product_attacment_download(request, handle=None, pk=None):

    attachment = get_object_or_404(ProductAttachment, product__handle=handle, pk=pk)
    can_download = False
    can_download = attachment.is_free or False
    if request.user.is_authenticated:
        can_download = True
    if can_download is False:
        return HttpResponseBadRequest()
    file = attachment.file.open(mode="rb")
    filename = attachment.file.name
    content_type, _ = mimetypes.guess_type(filename)
    response = FileResponse(file)
    response['Content-Type'] = content_type or 'application/octet-stream'
    response["Content-Disposition"] = f"attachment;filename={filename}"
    return response
