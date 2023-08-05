# -*- coding: utf-8 -*-
"""A set of fixtures to integrate Betamax with py.test.

.. autofunction:: betamax_session

"""

from __future__ import absolute_import

import pytest
import requests

from .. import recorder as betamax


@pytest.fixture
def betamax_session(request):
    """Generate a session that has Betamax already installed.

    This will create a new :class:`requests.Session` instance that is already
    using Betamax with a generated cassette name. The cassette name is
    generated by first using the module name from where the test is collected,
    then the class name (if it exists), and then the test function name. For
    example, if your test is in ``test_stuff.py`` and is the method
    ``TestStuffClass.test_stuff`` then your cassette name will be
    ``test_stuff_TestStuffClass_test_stuff``.

    :param request:
        A request object from pytest giving us context information for the
        fixture.
    :returns:
        An instantiated requests Session wrapped by Betamax.
    """
    cassette_name = ''

    if request.module is not None:
        cassette_name += request.module.__name__ + '.'

    if request.cls is not None:
        cassette_name += request.cls.__name__ + '.'

    cassette_name += request.function.__name__

    session = requests.Session()
    recorder = betamax.Betamax(session)
    recorder.use_cassette(cassette_name)
    recorder.start()
    request.addfinalizer(recorder.stop)
    return session
