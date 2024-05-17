
def add_to_dict(dictionary, key, value):
    """
    Method to add a key-value pair to a dictionary if the value is not None
    """
    if value is not None:
        dictionary[key] = value


###############################################################
################Pricing utilities##############################
def charm_price(price: float):
    """
    This method converts a price to (price-1).99
    """
    return price - 1 + 0.99

###############################################################
###############################################################