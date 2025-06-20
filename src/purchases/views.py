from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

import random 
import stripe 

from products.models import Product
from .models import Purchase

from micro_ecom.env import config


STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", default=None)
stripe.api_key = STRIPE_SECRET_KEY

BASE_ENDPOINT = "http://127.0.0.1:8000"


def purchase_start(request):
    if not request.method == "POST":
        return HttpResponseBadRequest()
    if not request.user.is_authenticated:
        return HttpResponseBadRequest()
    
    handle = request.POST.get("handle")
    obj = Product.objects.get(handle=handle)

    stripe_price_id = obj.stripe_price_id
    if stripe_price_id is None:
        return HttpResponseBadRequest()
    
    purchase = Purchase.objects.create(user=request.user, product=obj)
    request.session["purchase_id"] = purchase.id

    #Stripe checkout
    success_path = reverse('purchases:success')
    if not success_path.startswith("/"):
        success_path = f"/{success_path}"

    cancel_path = reverse('purchases:stopped')
    if not cancel_path.startswith("/"):
        cancel_path = f"/{cancel_path}"

    success_url = f"{BASE_ENDPOINT}{success_path}/"
    cancel_url = f"{BASE_ENDPOINT}{cancel_path}/"

    print(success_url, cancel_url)

    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                "price": stripe_price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )
    
    purchase.stripe_checkout_session_id = checkout_session.id
    purchase.save()
    
    return HttpResponseRedirect(checkout_session.url)


def purchase_success(request):
    purchase_id = request.session.get("purchase_id")
    if purchase_id:
        purchase = Purchase.objects.get(id=purchase_id)
        purchase.completed = True
        purchase.save()
    
    return HttpResponse("Success")


def purchase_stopped(request):
    return HttpResponse("Stopped")