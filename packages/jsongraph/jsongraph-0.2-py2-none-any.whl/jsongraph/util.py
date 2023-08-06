import url
from rdflib import ConjunctiveGraph, URIRef

# from rdflib.serializer import Serializer
# from rdflib.py3compat import b
# from rdflib.plugins.serializers.nquads import _nq_row


def is_url(text):
    """ Check if the given text looks like a URL. """
    if text is None:
        return False
    text = text.lower()
    return text.startswith('http://') or text.startswith('https://') or \
        text.startswith('urn:') or text.startswith('file://')


def safe_uriref(text):
    """ Escape a URL properly. """
    url_ = url.parse(text).sanitize().deuserinfo().canonical()
    return URIRef(url_.punycode().unicode())


def sparql_store(query_url, update_url):
    gs = ConjunctiveGraph('SPARQLUpdateStore')
    gs.open((query_url, update_url))
    return gs.store


class GraphException(Exception):
    pass


# class ContextNQuadsSerializer(Serializer):
#     """ Serialize graphs as nquads. """
#
#     def __init__(self, store):
#         super(ContextNQuadsSerializer, self).__init__(store)
#
#     def serialize(self, stream, base=None, encoding=None, **args):
#         encoding = self.encoding
#         for context in self.store:
#             for triple in context:
#                 stream.write(_nq_row(
#                     triple, self.store.identifier).encode(encoding, "replace"))
#         stream.write(b("\n"))
