"""Temporary script to rename Synco products to Dobry Plan in Stripe."""
import stripe
import os

stripe.api_key = os.environ["STRIPE_SECRET_KEY"]

# Get ALL products (including archived)
products = []
has_more = True
starting_after = None
while has_more:
    kwargs = {"limit": 100}
    if starting_after:
        kwargs["starting_after"] = starting_after
    batch = stripe.Product.list(**kwargs)
    products.extend(batch.data)
    has_more = batch.has_more
    if batch.data:
        starting_after = batch.data[-1].id

renamed = 0
for p in products:
    new_name = None
    new_desc = None
    if "Synco" in (p.name or ""):
        new_name = p.name.replace("Synco", "Dobry Plan")
    if "Synco" in (p.description or ""):
        new_desc = p.description.replace("Synco", "Dobry Plan")

    if new_name or new_desc:
        update = {}
        if new_name:
            update["name"] = new_name
        if new_desc:
            update["description"] = new_desc
        stripe.Product.modify(p.id, **update)
        print(f"  Renamed: {p.id} -> {new_name or p.name}")
        renamed += 1

print(f"\nDone. Renamed {renamed} products.")
