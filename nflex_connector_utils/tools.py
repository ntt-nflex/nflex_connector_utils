def serialize_list(data):
    """
        Convert all objects in a list to the CMP data structure by calling
        the ``serialize`` method on each element.

        Args:
            data (list): A list of objects to be serialized

        Returns:
            list: A list of dicts
    """

    return [d.serialize() for d in data]
