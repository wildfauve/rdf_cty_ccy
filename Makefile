.PHONY: all

RDFLOC := "rdfdata/"

all: build_cty_ccy_onto

build:
	@echo "Create New Wheel"
	@poetry version patch
	@poetry build


build_cty_ccy_onto:
	@echo "Downloading and building Currency and Country Ontologies"
	@poetry run build_onto --loc rdf_cty_ccy/rdfdata/


