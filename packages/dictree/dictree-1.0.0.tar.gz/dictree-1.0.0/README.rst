=======
dictree
=======
.. image:: https://travis-ci.org/tomokinakamaru/dictree.svg?branch=master
    :target: https://travis-ci.org/tomokinakamaru/dictree
    :alt: perth Build

About
=====
Tree structure with dict interface and wildcard feature.

Example
=======

.. sourcecode:: python

    from dictree import Dictree

    elt = Dictree()
    elt[()] = 'apple'
    elt[1, 2] = 'orange'
    elt[1, Dictree.WILDCARD] = 'banana'
    elt[1, 2, 3] = 'grape'
    elt[1, 2, 4] = 'peach'
    """
    [apple]--1-->[]--2-->[orange]--3-->[grape]
                  |                |
                  |                |-4--> [peach]
                  |--*-->[banana]
    """

    for k, v in elt.items():
        print(k, v)  # (), apple
                     # (1, 2), orange
                     # (1, WILDCARD), banana
                     # (1, 2, 3), grape
                     # (1, 2, 4), peach

    print(elt[1, 2])  # orange
    print(elt[1, 3])  # banana
    print(elt[1, 4])  # banana
    print(elt[(1,)])  # raises KeyError
