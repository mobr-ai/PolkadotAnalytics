import json

import SPARQLWrapper
from pyfuseki import FusekiQuery

from fuseki.server import FUSEKI_BASE_URL

class Ponto:
    fuseki_query:FusekiQuery = FusekiQuery(FUSEKI_BASE_URL, 'POnto')
    ponto_prefix = "http://www.mobr.ai/ontologies/ponto#"
    sparql_prefix = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX ponto: <http://www.mobr.ai/ontologies/ponto#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    """

    def check_name(short_name:str) -> str:
        return short_name.replace(Ponto.ponto_prefix, '').replace("ponto:", '')

    def extract_bindings(query_result:SPARQLWrapper.Wrapper.QueryResult) -> dict:
        rd = json.loads(query_result.response.read().decode("utf-8"))
        if type(rd) is dict:
            if 'results' in rd and 'bindings' in rd['results']:
                return rd['results']['bindings']

        return dict()

    def run_sparql(sparql_str, tripple_term="tt") -> list:
        values = list()

        fuseki_result = Ponto.fuseki_query.run_sparql(sparql_str)
        bindings = Ponto.extract_bindings(fuseki_result)
        if bindings:
            for b in bindings:
                if tripple_term in b:
                    values.append(b[tripple_term]['value'].replace(Ponto.ponto_prefix, ''))

        return values

    def get_entity_comment(entity_name:str) -> str:
        sparql_spec = f'ponto:{entity_name} rdfs:comment ?tt'
        sparql_str = Ponto.sparql_prefix + """
            SELECT DISTINCT ?tt
            WHERE
            {
                """ + sparql_spec + """
            }
        """

        return Ponto.run_sparql(sparql_str)

    def get_entity_class(entity_name:str) -> str:
        name = Ponto.check_name(entity_name)
        sparql_spec = f'ponto:{name} rdfs:subClassOf ?tt'
        sparql_str = Ponto.sparql_prefix + """
            SELECT ?tt
            WHERE
            {
                """ + sparql_spec + """
            }
        """

        return Ponto.run_sparql(sparql_str)

    def get_entity_subclasses(entity_name:str) -> list:
        name = Ponto.check_name(entity_name)
        sparql_spec = f'?tt rdfs:subClassOf ponto:{name}'
        sparql_str = Ponto.sparql_prefix + """
            SELECT ?tt
            WHERE
            {
                """ + sparql_spec + """
            }
        """

        return Ponto.run_sparql(sparql_str)

    def get_all_classes() -> set:
        sparql_str = Ponto.sparql_prefix + """
            SELECT DISTINCT ?tt
            WHERE {
            {
                ?tt a owl:Class .
            }
            UNION
            {
                ?tt rdfs:subClassOf ?class .
            }
            }
        """

        return Ponto.run_sparql(sparql_str)

    def get_all_properties() -> set:
        sparql_str = Ponto.sparql_prefix + """
            SELECT DISTINCT ?tt
            WHERE
            {
                ?s ?tt ?o .
            }
        """

        return Ponto.run_sparql(sparql_str)


    def define_entity(entity_name):
        name = Ponto.check_name(entity_name)
        sparql_spec = f'ponto:{name} rdfs:comment ?tt .'
        sparql_str = Ponto.sparql_prefix + """
            SELECT ?tt
            WHERE
            {
                """ + sparql_spec + """
            }
        """

        return Ponto.run_sparql(sparql_str)

    def get_all_instances() -> set:
        pass
