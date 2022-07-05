from typing import List, Optional

from rdflib import Literal, URIRef, XSD
from attrs import define
import rdflib.plugins.sparql.processor
from enum import Enum

from rdf_cty_ccy.graph import graph_query
from rdf_cty_ccy.common import fn, monad


class Filter:
    WithCurrency = 'withCurrency'


@define
class Currency:
    """
    <https://spec.edmcouncil.org/fibo/ontology/FND/Accounting/ISO4217-CurrencyCodes/NZD>
      a owl:NamedIndividual, fibo-fnd-acc-cur:CurrencyIdentifier ;
      rdfs:label "NZD" ;
      skos:definition "the currency identifier for New Zealand Dollar"@en ;
      lcc-lr:denotes <https://spec.edmcouncil.org/fibo/ontology/FND/Accounting/ISO4217-CurrencyCodes/NewZealandDollar> ;
      lcc-lr:hasTag "NZD" ;
      lcc-lr:identifies <https://spec.edmcouncil.org/fibo/ontology/FND/Accounting/ISO4217-CurrencyCodes/NewZealandDollar> ;
      lcc-lr:isMemberOf <https://spec.edmcouncil.org/fibo/ontology/FND/Accounting/ISO4217-CurrencyCodes/ISO4217-CodeSet> .
    """
    currency_uri: URIRef
    identifies: URIRef
    label: Literal


@define
class Country:
    """
    <https://www.omg.org/spec/LCC/Countries/ISO3166-1-CountryCodes/NZL>
      a owl:NamedIndividual, lcc-cr:Alpha3Code ;
      skos:definition "Alpha-3 country code for New Zealand" ;
      rdfs:label "NZL" ;
      lcc-lr:hasTag "NZL"^^xsd:string ;
      lcc-lr:denotes <https://www.omg.org/spec/LCC/Countries/ISO3166-1-CountryCodes/NewZealand> ;
      lcc-lr:identifies <https://www.omg.org/spec/LCC/Countries/ISO3166-1-CountryCodes/NewZealand> ;
      lcc-lr:isMemberOf <https://www.omg.org/spec/LCC/Countries/ISO3166-1-CountryCodes/ISO3166-1-Alpha3-CodeSet> ;
      rdfs:isDefinedBy <https://www.omg.org/spec/LCC/Countries/ISO3166-1-CountryCodes/> .
    """
    country_uri: URIRef = None
    identifies: URIRef = None
    label: Literal = None
    currency: Currency = None


def by_country_code(code: str, filters: List[Optional[Filter]] = []) -> Optional[Country]:
    """
    Takes an ISO3166 Alpha-3 country code and returns a single country/currency result.
    If there are no results, None is returned.  If a code as string was not provided, None is returned.

    :param code: A single ISO3166 3 Alpha country code
    :param filters: An Optional List of filters directing what should be returned; from the Filter enum
    :return: Country object with associated Currency
    """
    if not isinstance(code, str):
        return None
    lit = convert_literal(code)
    if lit.is_left():
        return None
    return build(Country(), find_by_code(cty_tag_maximal_query, lit.value), filters)


def by_country_uri(uri: str, filters: List[Optional[Filter]] = []) -> Optional[Country]:
    if not isinstance(uri, str):
        return None
    uriref = convert_uri(uri)
    if uriref.is_left():
        return None
    return build(Country(country_uri=uriref.value), find_by_uri(cty_uri_maximal_query, uriref.value), filters)


@monad.monadic_try()
def convert_literal(lit):
    return Literal(lit, datatype=XSD.string)


@monad.monadic_try()
def convert_uri(uri):
    return URIRef(uri)


def find_by_code(query_fn, lit_code):
    return fn.first([r for r in graph_query.sparql(query_fn(lit_code))])


def find_by_uri(query_fn, uri):
    return fn.first([r for r in graph_query.sparql(query_fn(uri))])


def build(country: Country, result: rdflib.query.ResultRow, filters: List[Optional[Filter]]) -> Optional[Country]:
    if not result:
        return None

    if not country.country_uri:
        country.country_uri = result.cty

    country.identifies = result.cty_identifies
    country.label = result.cty_label

    if Filter.WithCurrency in filters:
        country.currency = Currency(currency_uri=result.ccy_code_uri,
                                    identifies=result.ccy_identifies,
                                    label=result.ccy_label)
    return country


def cty_tag_maximal_query(cty_tag: Literal) -> rdflib.plugins.sparql.processor.SPARQLResult:
    return """
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
    PREFIX lcc-lr: <https://www.omg.org/spec/LCC/Languages/LanguageRepresentation/>
    PREFIX lcc-cr: <https://www.omg.org/spec/LCC/Countries/CountryRepresentation/>

    SELECT ?cty ?cty_identifies ?cty_label ?ccy_identifies ?ccy_code_uri ?ccy_label
    WHERE {{
      ?cty lcc-lr:hasTag {cty_tag} ;
           rdfs:label ?cty_label ; 
           lcc-lr:identifies ?cty_identifies .
      ?ccy_identifies lcc-cr:isUsedBy ?cty_identifies .
      ?ccy_code_uri lcc-lr:identifies ?ccy_identifies ;
                   rdfs:label ?ccy_label  
    }}
    """.format(cty_tag=cty_tag.n3())


def cty_uri_maximal_query(cty_uri: URIRef) -> rdflib.plugins.sparql.processor.SPARQLResult:
    return """
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
    PREFIX lcc-lr: <https://www.omg.org/spec/LCC/Languages/LanguageRepresentation/>
    PREFIX lcc-cr: <https://www.omg.org/spec/LCC/Countries/CountryRepresentation/>

    SELECT ?cty ?cty_identifies ?cty_label ?ccy_identifies ?ccy_code_uri ?ccy_label
    WHERE {{
      {cty_uri} rdfs:label ?cty_label ; 
           lcc-lr:identifies ?cty_identifies .
      ?ccy_identifies lcc-cr:isUsedBy ?cty_identifies .
      ?ccy_code_uri lcc-lr:identifies ?ccy_identifies ;
                   rdfs:label ?ccy_label  
    }}
    """.format(cty_uri=cty_uri.n3())
