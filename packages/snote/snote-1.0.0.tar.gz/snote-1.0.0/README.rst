=====
snote
=====
.. image:: https://travis-ci.org/tomokinakamaru/snote.svg?branch=master
    :target: https://travis-ci.org/tomokinakamaru/snote
    :alt: perth Build

About
=====

A tool for generating signed, time-limited & tagged tokens of python objects.

Example
=======

.. sourcecode:: python

    import snote

    # instanciate snote.Codec with your secret key
    sncodec = snote.Codec('secret-key')

    # the object to encode
    obj = {'user_id': 1}
    encoded_obj = sncodec.encode(obj)

    # retrieve the token to carry around
    token = encoded_obj.token
    print(encoded_obj.timestamp)  # timestamp of token generation
    print(encoded_obj.tag)  # use this tag to manage tokens' validity

    # decode from token
    decoded_obj = sncodec.decode(token)
    print(decoded_obj.obj)  # {'user_id': 1}
    print(decoded_obj.tag == encoded_obj.tag)  # True
    print(decoded_obj.is_expired(10))  # if the token age is less than 10 secs
