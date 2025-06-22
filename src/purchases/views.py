from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse

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
    request.session['purchase_id'] = purchase.id

    success_path = reverse("purchases:success")
    if not success_path.startswith("/"):
        success_path = f"/{success_path}"

    cancel_path = reverse("purchases:stopped")
    success_url = f"{BASE_ENDPOINT}{success_path}?session_id={{CHECKOUT_SESSION_ID}}"
    cancel_url = f"{BASE_ENDPOINT}{cancel_path}"
    print(success_url, cancel_url)
    
    checkout_session = stripe.checkout.Session.create(
        line_items = [
            {
                "price": stripe_price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url
    )
    purchase.stripe_checkout_session_id = checkout_session.id
    purchase.save()
    return HttpResponseRedirect(checkout_session.url)


def purchase_success(request):
    session_id = request.GET.get("session_id")
    if not session_id:
        return HttpResponseBadRequest("Missing session ID")

    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except stripe.error.StripeError:
        return HttpResponseBadRequest("Invalid session ID")

    if session.payment_status == "paid":
        try:
            purchase = Purchase.objects.get(stripe_checkout_session_id=session_id)
            purchase.completed = True
            purchase.save()
            del request.session['purchase_id']
        except Purchase.DoesNotExist:
            return HttpResponseBadRequest("Purchase not found")

        # return HttpResponse("Success: payment completed!")
        return HttpResponseRedirect(purchase.product.get_absolute_url())
    else:
        return HttpResponse("Payment not completed.")


def purchase_stopped(request):
    purchase_id = request.session.get("purchase_id")

    if purchase_id:
        purchase = Purchase.objects.get(id=purchase_id)
        product = purchase.product
        del request.session['purchase_id']
        return HttpResponseRedirect(product.get_absolute_url())
    return HttpResponse("Stopped")