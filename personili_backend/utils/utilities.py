
def add_to_dict(dictionary, key, value):
    """
    Method to add a key-value pair to a dictionary if the value is not None
    """
    if value is not None:
        dictionary[key] = value