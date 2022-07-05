# RDF Country and Currency Graph Library

This library builds an RDF graph of country and currency codes based on the following ontologies:

+ https://www.omg.org/spec/LCC/Countries/ISO3166-1-CountryCodes/
+ https://spec.edmcouncil.org/fibo/ontology/FND/Accounting/ISO4217-CurrencyCodes/

Both of these graphs are in Turtle format and are used extensively in the [FIBO ontologies](https://github.com/edmcouncil/fibo)

The Library is designed to support querying these triples in 3 modes:

+ Using the Python RDFLib library.  The graph is queried using the RDFLib triples mode.  Returns RDF triples.
+ Using a SPARQL query.  Returns an RDFLib SPARQL result.
+ Via an OO query approach, which returns country and currency objects. 

# Usage

## RDFLib Triples Mode


## SPARQL Mode

## OO Mode

```python
from rdf_cty_ccy.query import query as Q

country = Q.by_country_code(code='NZL')

country.country_uri             # => rdflib.term.URIRef('https://www.omg.org/spec/LCC/Countries/ISO3166-1-CountryCodes/NZL')
str(country.country_uri)        # => 'https://www.omg.org/spec/LCC/Countries/ISO3166-1-CountryCodes/NZL'
```

Provide the currency filter to obtain the currency properties for the country.

```python
country = Q.by_country_code(code='NZL', filters=[Q.Filter.WithCurrency])

country.currency.currency_uri   # => rdflib.term.URIRef('https://spec.edmcouncil.org/fibo/ontology/FND/Accounting/ISO4217-CurrencyCodes/NZD')

```

