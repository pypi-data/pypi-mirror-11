try:
    import cPickle as pickle
except ImportError:
    import pickle

from django.core import signing

from django_q.conf import Conf

BadSignature = signing.BadSignature


class SignedPackage(object):
    """
    Wraps Django's signing module with custom Pickle serializer
    """

    @staticmethod
    def dumps(obj, compressed=Conf.COMPRESSED):
        return signing.dumps(obj,
                             key=Conf.SECRET_KEY,
                             salt='django_q.q',
                             compress=compressed,
                             serializer=PickleSerializer)

    @staticmethod
    def loads(obj):
        return signing.loads(obj,
                             key=Conf.SECRET_KEY,
                             salt='django_q.q',
                             serializer=PickleSerializer)


class PickleSerializer(object):
    """
    Simple wrapper around Pickle for signing.dumps and
    signing.loads.
    """

    @staticmethod
    def dumps(obj):
        return pickle.dumps(obj)

    @staticmethod
    def loads(data):
        return pickle.loads(data)
