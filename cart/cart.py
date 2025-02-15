from shop.models import Products


class Cart():
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_cart_key')
        if 'session_cart_key' not in request.session:
            cart = self.session['session_cart_key'] = {}
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id] += quantity 
        else:
            self.cart[product_id] = quantity
        self.session.modified = True

    def __len__(self):
        return len(self.cart)
    
    def get_items(self):
        prods_ids = self.cart.keys()
        prods = Products.objects.filter(id__in=prods_ids)
        return prods
    
    def get_items_ids(self):
        return self.cart.keys()
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, prod, quantity):
        prod_id = str(prod)
        quantity = int(quantity)
        self.cart[prod_id] = quantity
        self.session.modified = True

        
    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True 

    def cart_total(self):
        qty = self.cart
        prod_ids = self.cart.keys()
        prods = Products.objects.filter(id__in=prod_ids)
        total = 0
        for key, value in qty.items():
            key = int(key)
            for prod in prods:
                if prod.id == key:
                    quantity = int(value)
                    if prod.discount_price is not None:
                        total += (prod.discount_price * quantity)
                    else:
                        total += (prod.price * quantity)
        return round(total, 2)
