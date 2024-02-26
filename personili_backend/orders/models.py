from django.db import models

# Standard imports
from uuid import uuid4
from datetime import datetime

# Model imports
from accounts.models import AccountProfile, DeliveryAddress, PaymentMethod
from accounts.models import TimeStampedModel
from personalizables.models import Product 




#########################################
#             Cart model                #
#########################################
class Cart(TimeStampedModel):
    """
    Cart model has the following fields :
    - id (primary key)
    - user_profile (linked to the user profile table)
    - total_amount (total amount of the cart after applying discounts)
    - open (boolean field to indicate if the cart is open or not)
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    account_profile = models.ForeignKey(AccountProfile, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    open = models.BooleanField(default=True)


    def __str__(self):
        return f'{self.account_profile} - {self.total_amount} - {self.open}'
    

    @classmethod
    def is_there_an_open_cart(cls, account_profile: AccountProfile) -> bool:
        """
        This method will check if there is a cart which is open, if yes then it will return True, otherwise
        it will return False
        """
        try:
            cart = cls.objects.get(account_profile=account_profile, open=True)
            return True
        except cls.DoesNotExist:
            return False
    
    @classmethod
    def create_or_get_the_cart(cls, account_profile: AccountProfile):
        """
        This method will check if there is a cart which is open, if yes then it will return it, otherwise
        it will create a new one and return it as well
        """
        try:
            cart = cls.objects.get(account_profile=account_profile, open=True)
        except cls.DoesNotExist:
            cart = cls.objects.create(account_profile=account_profile, open=True)
        return cart

    def add_items_to_cart(self, products:list[Product]):
        """
        This method takes a list of products, for each product it creates a new cart item
        """
        for product in products:
            CartItem.objects.create(
                cart=self,
                product=product,
                quantity=1,
                sub_total=product.price
            )
        return self

    def remove_items_from_cart(self, cart_items_id:list[str]):
        """
        This method takes a list of products, for each product it removes the cart item
        """
        for cart_item_id in cart_items_id:
            CartItem.objects.get(id=cart_item_id).delete()

    def update_carte_items(self, cart_items_id:list[str], quantities:list[int]):
        """
        This method takes a list of cart items ids and a list of quantities, it updates the quantities of the cart items
        """
        for cart_item_id, quantity in zip(cart_items_id, quantities):
            cart_item = CartItem.objects.get(id=cart_item_id)
            cart_item.quantity = quantity
            cart_item.sub_total = cart_item.product.price * quantity
            cart_item.save()      
        
    def validate_the_cart(self, account_profile: AccountProfile, delivery_address_id: str, payment_method_id: str):
        """
        This method will transform the cart and its items into an order with its order items
        - First it will create the order, then it will create the order items and finally it will create the bill
        """
        # Create the order
        order = Order.objects.create(
            account_profile=account_profile,
            delivery_address=delivery_address_id,
            payment_method=payment_method_id,
            order_date=datetime.now(),
            total_amount=self.total_amount
        )

        # Create the order items
        for cart_item in self.cart_items_of_a_cart.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                sub_total=cart_item.sub_total
            )

        # Create the bill
        bill = Bill.objects.create(
            order=order,
            total_amount=order.total_amount
        )

        # Create the shipping 
        return order, bill
 

    def get_cart_items(self):
        """
        This method returns the cart items of a cart, for each cart item it returns its details
        as well as the product details associated to it
        """
        cart_items = []
        for cart_item in self.cart_items_of_a_cart.all():
            cart_items.append({
                'cart_item_id': cart_item.id,
                'quantity': cart_item.quantity,
                'sub_total': cart_item.sub_total,
                'product_details': Product.objects.get(id=cart_item.product.id).get_full_product_description()
            })
            
        return cart_items

#########################################
#         Cart Item model               #
#########################################
class CartItem(TimeStampedModel):
    """
    Each cart item is linked to a cart and a product, it has a quantity and a sub total
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items_of_a_cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items_of_a_product')
    quantity = models.IntegerField(default=1)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product.name} - {self.quantity} - {self.sub_total}'


#########################################
#             Order model               #
#########################################
class Order(TimeStampedModel):
    """
    Order model has the following fields :
    - id (primary key)
    - account_profile (linked to the user profile table)
    - order_date (date the order was placed)
    - total_amount (total amount of the order)
    - status (Pending, Processing, Shipped, Delivered, Cancelled) 
    - delivery_address (linked to the delivery address table)
    - payment_method (linked to the payment method table)
    """
    # Status choices
    PENDING = 'Pending'
    PROCESSING = 'Processing'
    CONFIRMED = 'Confirmed'
    CANCELLED = 'Cancelled'
    ORDER_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (CONFIRMED, 'Confirmed'),
        (CANCELLED, 'Cancelled')
    ]

    # Allowed currencies
    DA = 'DA'
    EUR = 'EUR'
    USD = 'USD'
    CURRENCY_CHOICES = [
        (DA, 'DA'),
        (EUR, 'EUR'),
        (USD, 'USD')
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    account_profile = models.ForeignKey(AccountProfile, on_delete=models.CASCADE, related_name='orders_of_an_account')
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default=DA, choices=CURRENCY_CHOICES)
    order_status = models.CharField(max_length=20, default=PENDING, choices=ORDER_STATUS_CHOICES)
    delivery_address = models.ForeignKey(DeliveryAddress, on_delete=models.DO_NOTHING)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.account_profile} - {self.order_date} - {self.status}'
    
    
    def get_related_bill(self):
        """
        Returns the bill related to this order
        """
        return self.bill_set.all().first()
    
    @classmethod
    def create_order_and_its_order_items_and_bill(cls, account_profile: str,
                                                   delivery_address: str, 
                                                   payment_method: str, 
                                                   products_ids_with_quantities_and_sub_totals):
        """
        This method will take a list of products ids (each product id with their respective quantity and sub_total),
        The delivery address id,
        The payment method id and the user profile id,
        The user profiel id or the user id (the user profile id can be obtained from the user id),
        The method will start by creating the order, then it will create the order items and finally it will create the bill.
        Some attributes like the total in the order and the total in the bill will be calculated in the method.
        """

        # Create the order
        order = cls.objects.create (
            account_profile=account_profile,
            delivery_address=delivery_address,
            order_date=datetime.now(),
            payment_method=payment_method,
            total_amount=sum([float(sub_total) for _, _, sub_total in products_ids_with_quantities_and_sub_totals])
        )

        # Create the order items
        for order_item_tuple in products_ids_with_quantities_and_sub_totals:

            for product_id, quantity, sub_total in order_item_tuple:
                OrderItem.objects.create(
                    order=order,
                    product=product_id,
                    quantity=quantity,
                    sub_total=sub_total
            )

        # Create the bill
        bill = Bill.objects.create(
            order=order,
            total_amount=order.total_amount
        )
        return order, bill
    
     
#########################################
#             OrderItem model           #
#########################################
class OrderItem(TimeStampedModel):
    """
    OrderItem model has the following fields :
    - id (primary key)
    - order (linked to the order table)
    - product (linked to the product table)
    - quantity (quantity of the product ordered)
    - sub_total (sub total of the product ordered)
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items_of_an_order')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items_of_a_product')
    quantity = models.IntegerField(default=1)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)


#########################################
#             Bill model                #
#########################################
class Bill(TimeStampedModel):
    """
    Bill model has the following fields :
    - id (primary key)
    - order (linked to the order table)
    - total_amount (total amount of the order)
    - payment status
    - billing_address
    - payment_method
    """
    # Payment status choices
    PAID = 'Paid'
    UNPAID = 'Unpaid'
    PAYMENT_STATUS_CHOICES = [
        (PAID, 'Paid'),
        (UNPAID, 'Unpaid')
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, related_name='bill_of_an_order')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, default=UNPAID, choices=PAYMENT_STATUS_CHOICES)
    billing_address = models.ForeignKey(DeliveryAddress, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.order} - {self.total_amount} - {self.payment_status}'



#########################################
#          Delivery methods model       #
#########################################
class DeliveryMethod(TimeStampedModel):
    """
    DeliveryMethod model has the following fields :
    - id (primary key)
    - name (name of the delivery method)
    - description (description of the delivery method)
    - cost (cost of the delivery method)
    - delivery_time (estimated delivery time)
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_time = models.DurationField()

    def __str__(self):
        return f'{self.name} - {self.cost} - {self.delivery_time}'

#########################################
#          Delivery model               #
#########################################
class Delivery(TimeStampedModel):
    """
    Delivery table has the following fields :
    - id
    - order (linked to the order table)
    - delivery_date (estimated_date of delivery)
    - status (Pending, Shipped, Delivered, Cancelled)
    - delivery_address (linked to the delivery address table)
    - delivery_method (linked to the delivery method table)
    """
    # Status choices
    PENDING = 'Pending'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'
    CANCELLED = 'Cancelled'
    DELIVERY_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELLED, 'Cancelled')
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    delivery_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default=PENDING, choices=DELIVERY_STATUS_CHOICES)
    delivery_address = models.ForeignKey(DeliveryAddress, on_delete=models.DO_NOTHING)
    delivery_method = models.ForeignKey(DeliveryMethod, on_delete=models.DO_NOTHING)


#########################################
#      Delivery Item model              #
#########################################
class DeliveryItem(TimeStampedModel):
    """
    DeliveryItem model has the following fields :
    - id (primary key)
    - delivery (linked to the delivery table)
    - order_item (linked to the order item table)
    - quantity (quantity of the product ordered)
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    order_item = models.ForeignKey(OrderItem, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return f'{self.delivery.id} - {self.order_item.id} - {self.quantity}'
