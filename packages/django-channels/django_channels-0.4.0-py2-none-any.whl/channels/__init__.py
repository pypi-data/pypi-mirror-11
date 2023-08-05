# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys


_BACKENDS = {}


def _load_module(name):
    __import__(name)
    return sys.modules[name]


def _load_backend(name):
    try:
        return _BACKENDS[name]
    except KeyError:
        module_name, klass_name = name.rsplit(".", 1)
        module = _load_module(module_name)
        _BACKENDS[name] = getattr(module, klass_name)
        return _BACKENDS[name]


def send(message, fail_silently=False, options=None):
    """Send a notification to all configured backends

    :param message: A message
    :type message: str | unicode
    :type fail_silently: bool
    :type options: dict
    """
    from django.conf import settings

    for klass, config in settings.CHANNELS["CHANNELS"].items():
        channel = _load_backend(klass)(**config)
        channel.send(message, fail_silently=fail_silently, options=options)
