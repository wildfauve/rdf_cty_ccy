from rdflib import XSD, Literal

from rdf_cty_ccy.graph import graph, graph_query
from rdf_cty_ccy.graph import rdf_prefix as P

def setup_module():
    read_graph()

def it_finds_triples_for_a_country_has_tag():
    result = graph_query.query((None, P.lcc_lr.hasTag, Literal("NZL", datatype=XSD.string)))

    assert len(result) == 1

    s, _, _ = result[0]

    assert s == P.lcc_3166_1.NZL

def it_searches_for_triples_using_sparql_query():
    result = graph_query.sparql(nzl_sparql_query())

    args = [(row.cty, row.name) for row in result]

    cty, name = args[0]

    assert cty == P.lcc_3166_1.NZL
    assert name == P.lcc_3166_1.NewZealand


def it_searches_for_country_and_connects_to_currency():
    result = graph_query.sparql(nzl_to_nzd_sparql_query())

    args = [(row.cty, row.cty_id, row.ccy_id, row.ccy_code_id, row.ccy_tag) for row in result]

    cty, cty_id, ccy_id, ccy_code_id, ccy_tag = args[0]

    assert cty == P.lcc_3166_1.NZL
    assert cty_id == P.lcc_3166_1.NewZealand
    assert ccy_id == P.fibo_fnd_acc_4217.NewZealandDollar
    assert ccy_code_id == P.fibo_fnd_acc_4217.NZD
    assert ccy_tag == Literal('NZD')

#
# Helpers
#
def read_graph():
    return graph.graph()

def nzl_sparql_query():
    return """
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX lcc-lr: <https://www.omg.org/spec/LCC/Languages/LanguageRepresentation/>
    
    SELECT ?cty ?name
    WHERE {
      ?cty lcc-lr:hasTag "NZL"^^xsd:string ;
           lcc-lr:identifies ?name
    }
    """

def nzl_to_nzd_sparql_query():
    return """
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX lcc-lr: <https://www.omg.org/spec/LCC/Languages/LanguageRepresentation/>
    PREFIX lcc-cr: <https://www.omg.org/spec/LCC/Countries/CountryRepresentation/>
    
    SELECT ?cty ?cty_id ?ccy_id ?ccy_code_id ?ccy_tag
    WHERE {
      ?cty lcc-lr:hasTag "NZL"^^xsd:string ;
           lcc-lr:identifies ?cty_id .
      ?ccy_id lcc-cr:isUsedBy ?cty_id .
      ?ccy_code_id lcc-lr:identifies ?ccy_id ;
                   lcc-lr:hasTag ?ccy_tag  
    }
    """