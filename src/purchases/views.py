from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
import random 

from products.models import Product
from .models import Purchase


def purchase_start(request):
    if not request.method == "POST":
        return HttpResponseBadRequest()
    if not request.user.is_authenticated:
        return HttpResponseBadRequest()
    
    handle = request.POST.get("handle")
    obj = Product.objects.get(handle=handle)
    purchase = Purchase.objects.create(user=request.user, product=obj)

    request.session["purchase_id"] = purchase.id

    number = random.randint(0, 1)
    print(number)

    if number == 1:
        return HttpResponseRedirect ('/purchases/success')
    
    return HttpResponseRedirect ('/purchases/stopped')


def purchase_success(request):
    purchase_id = request.session.get("purchase_id")
    if purchase_id:
        purchase = Purchase.objects.get(id=purchase_id)
        purchase.completed = True
        purchase.save()
    
    return HttpResponse("Success")


def purchase_stopped(request):
    return HttpResponse("Stopped")