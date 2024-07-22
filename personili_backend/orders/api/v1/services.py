from orders.models import Cart, CartItem, Order, OrderItem


##############################   Cart Management  ##############################
def get_current_cart(account_profile_id: str = None, cart_id:str = None):
    """
    This function returns the current cart for the user, if it exists.
    """
    # Check if there is an open cart for this account profile id
    open_cart = Cart.is_there_an_open_cart(account_profile_id=account_profile_id)


def add_item_to_cart(account_profile_id: str, product_variant_id: str, quantity: int=1):
    """
    Add a product variant to the cart, then return the updated cart
    """
    pass

def remove_item_from_cart(account_profile_id: str, product_variant_id: str):
    """
    Remove a product variant from the cart, if there 
    """
    pass

def update_item_quantity(account_profile_id: str, product_variant_id: str, quantity: int):
    """
    Update the quantity of a product variant in the cart
    """
    pass

def validate_cart(cart_id: str):
    """
    - Validate the cart, transform the cart into an order and the cart items into order items
    - The method should use select for update to create a lock on the following entities:
    - The method should update the quantity of the product variant in the cart item
    """
    pass