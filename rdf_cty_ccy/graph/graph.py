from rdflib import Graph
from simple_memory_cache import GLOBAL_CACHE

from . import binding

graph_cache = GLOBAL_CACHE.MemoryCachedVar('graph_cache')

currency_code_triples = "rdf_cty_ccy/rdfdata/ISO3166-1-CountryCodes.ttl"
country_code_triples = "rdf_cty_ccy/rdfdata/ISO4217-CurrencyCodes.ttl"

def graph():
    return graph_cache.get()

def invalidate_cache():
    graph_cache.invalidate()
    pass

@graph_cache.on_first_access
def build_graph():
    g = initgraph()
    g.parse(currency_code_triples)
    g.parse(country_code_triples)
    return g

def initgraph() -> Graph:
    return binding.bind(rdf_graph())

def rdf_graph():
    return Graph()