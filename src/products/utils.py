import stripe 

from micro_ecom.env import config

STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", default=None)
stripe.api_key = STRIPE_SECRET_KEY


def product_sales_pipeline(product_name="Test product", product_price=1000):
    # 1. Create the Product
    stripe_product_obj = stripe.Product.create(name=product_name)
    stripe_product_id = stripe_product_obj.id

    # 2. Create the Price (associated with the Product)
    stripe_price_obj = stripe.Price.create(
        product=stripe_product_id,
        unit_amount=product_price,
        currency="usd",
    )
    stripe_price_id = stripe_price_obj.id

    # 3. Define URLs for the Checkout Session
    base_endpoint = "http://127.0.0.1:8000"
    success_url = f"{base_endpoint}/purchases/success/"
    cancel_url = f"{base_endpoint}/purchases/stopped/"

    # 4. Create the Checkout Session
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

    print(checkout_session.url)
