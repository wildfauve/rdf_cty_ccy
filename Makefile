.PHONY: all

RDFLOC := "rdfdata/"

all: build_cty_ccy_onto

build_cty_ccy_onto:
	@echo "Downloading and building Currency and Country Ontologies"
	@poetry run poetry run build_onto --loc rdf_cty_ccy/rdfdata/

