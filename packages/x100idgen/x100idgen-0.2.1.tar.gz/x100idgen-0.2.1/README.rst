NAME
====

x100idgen - Id generator require no centralized authority


SYNOPSIS
========

.. code::

    import x100idgen

    def get_id(hash_string):
        idgen = x100idgen.IdGen()
        your_id = idgen.gen_id(hash_string)
        return (your_id)

    def validate_id(your_id):
        idgen = x100idgen.IdGen()
        if idgen.validate_id(your_id):
            return True
        else:
            return False

    if __name__ == '__main__':
        hash_string = "111.206.116.190Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/8.0.6 Safari/600.6.3"
        your_id = get_id(hash_string)
        print("Get id : " + your_id)

        id_valid = str(validate_id(your_id))
        print("The id " + your_id + " is " + id_valid)

Ouput:

.. code::

    Get id : ytmaWHUzDikIGwOLl6
    The id ytmaWHUzDikIGwOLl6 is True


DESCRIPTION
===========

x100idgen is an id generator require no centralized authority like uuidgen, shorter and more customizable.

This module helps generate unique ids like 'ytmaWHUzDikIGwOLl6' (/^[0-9a-zA-Z]{18}$/) easy and fast.


