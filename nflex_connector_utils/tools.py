import os


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


def vcr_cassette_context(function):
    """
        Enclose decorated function into vcr.use_cassette context.

        Args:
            function (function): inner function to enclose

        Returns:
            function: wrapper of inner function
    """
    def wrapper(*args, **kwargs):
        if 'DEBUG_VCR' in os.environ:
            import vcr
            with vcr.use_cassette('vcr.yaml', record_mode='new_episodes',
                                  ignore_hosts=['192.168.42.24']):
                return function(*args, **kwargs)
        else:
            return function(*args, **kwargs)

    return wrapper
