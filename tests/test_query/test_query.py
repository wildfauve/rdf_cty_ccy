from rdflib import Literal

from rdf_cty_ccy.query import query as Q
from rdf_cty_ccy.graph import rdf_prefix as P
from rdf_cty_ccy.graph import graph

def setup_module():
    graph.graph()

def it_returns_none_when_cty_code_not_string():
    assert Q.by_country_code({}) == None

def it_returns_none_when_cty_code_is_not_found():
    assert Q.by_country_code("ABC") == None

def it_returns_a_single_country():
    result = Q.by_country_code(code='NZL')

    assert result.country_uri == P.lcc_3166_1.NZL
    assert result.identifies == P.lcc_3166_1.NewZealand
    assert result.label == Literal('NZL')

def it_indicates_the_code_set_of_the_cty_code():
    result = Q.by_country_code(code='NZL')

    assert result.code_type == P.lcc_3166_1.term("ISO3166-1-Alpha3-CodeSet")

def it_returns_a_single_country_with_currency():
    result = Q.by_country_code(code='NZL', filters=[Q.Filter.WithCurrency])

    assert result.currency.currency_uri == P.fibo_fnd_acc_4217.NZD
    assert result.currency.identifies == P.fibo_fnd_acc_4217.NewZealandDollar
    assert result.currency.label == Literal('NZD')

def it_returns_a_single_country_based_on_country_uri():
    result = Q.by_country_uri(uri='https://www.omg.org/spec/LCC/Countries/ISO3166-1-CountryCodes/NZL')

    assert result.country_uri == P.lcc_3166_1.NZL
    assert result.identifies == P.lcc_3166_1.NewZealand
    assert result.label == Literal('NZL')

def it_finds_an_alpha_2_cty_code():
    result = Q.by_country_code(code='NZ')

    assert result.country_uri == P.lcc_3166_1.NZ
    assert result.identifies == P.lcc_3166_1.NewZealand
    assert result.label == Literal('NZ')
    assert result.code_type == P.lcc_3166_1.term("ISO3166-1-Alpha2-CodeSet")
