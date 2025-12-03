from uuid import uuid4

def unique_file_name():
    """
    Returns a unique string
    """
    return uuid4().hex
