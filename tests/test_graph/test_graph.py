from rdf_cty_ccy.graph import graph


def it_reads_the_ccy_and_cty_graph_and_returns_the_right_number_of_nodes():
    g = graph.graph()

    assert len(g.all_nodes()) == 5924


def it_finds_a_country_by_has_tag_code():
    pass