import json
import SPARQLWrapper
from rdflib import Graph
from pyfuseki import FusekiQuery, FusekiUpdate

class KBM:
    """
    Knowledge Base Management class

    This is a static class to create an abstraction layer on top of the RDF triplestore SPARQL engine

    """

    ponto_prefix = "http://www.mobr.ai/ontologies/ponto#"
    sparql_prefix = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX ponto: <http://www.mobr.ai/ontologies/ponto#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    """
    fuseki_base_url = "http://127.0.0.1:3030"
    fuseki_endpoint = "POnto"

    # utils
    ###

    def check_name(short_name:str) -> str:
        return short_name.replace(KBM.ponto_prefix, '').replace("ponto:", '')

    def extract_bindings(query_result:SPARQLWrapper.Wrapper.QueryResult) -> dict:
        rd = json.loads(query_result.response.read().decode("utf-8"))
        if type(rd) is dict:
            if 'results' in rd and 'bindings' in rd['results']:
                return rd['results']['bindings']

        return dict()


    # crud
    ###
    def inject_turtle_file(turtle_file_uri:str):
        g = Graph()
        g.parse(turtle_file_uri, format='ttl')

        fuseki = FusekiUpdate(KBM.fuseki_base_url, KBM.fuseki_endpoint)
        fuseki.insert_graph(g)

    def get_triples_with_entity(entity_name:str, spo:str='s') -> str:
        name = KBM.check_name(entity_name)

        if spo == 's':
            sparql_spec = f'ponto:{name} ?p ?o'
        elif spo == 'p':
            sparql_spec = f'?s ponto:{name} ?o'
        else:
            sparql_spec = f'?s ?p ponto:{name}'

        sparql_str = KBM.sparql_prefix + """
            SELECT *
            WHERE
            {
                """ + sparql_spec + """
            }
        """

        return KBM.run_sparql(sparql_str)

    def update_entity(entity_old_name:str, entity_new_name:str, spo:str='s'):
        old_name = KBM.check_name(entity_old_name)
        new_name = KBM.check_name(entity_new_name)

        if spo == 's':
            sparql_old = f'ponto:{old_name} ?p ?o .'
            sparql_new = f'ponto:{new_name} ?p ?o .'
        elif spo == 'p':
            sparql_old = f'?s ponto:{old_name} ?o .'
            sparql_new = f'?s ponto:{new_name} ?o .'
        else:
            sparql_old = f'?s ?p ponto:{old_name} .'
            sparql_new = f'?s ?p ponto:{new_name} .'

        sparql_str = KBM.sparql_prefix + """
            DELETE {
                """ + sparql_old + """
            }
            INSERT
            {
                """ + sparql_new + """
            }
            WHERE
            {
                """ + sparql_old + """
            }
        """

        fuseki = FusekiUpdate(KBM.fuseki_base_url, KBM.fuseki_endpoint)
        fuseki.run_sparql(sparql_str=sparql_str)

    def delete_entity(entity_name:str, spo:str='s'):
        name = KBM.check_name(entity_name)
        if spo == 's':
            sparql_spec = f'ponto:{name} ?p ?o .'
        elif spo == 'p':
            sparql_spec = f'?s ponto:{name} ?o .'
        else:
            sparql_spec = f'?s ?p ponto:{name} .'

        sparql_str = KBM.sparql_prefix + """
            delete where
            {
                """ + sparql_spec + """
            }
        """

        fuseki = FusekiUpdate(KBM.fuseki_base_url, KBM.fuseki_endpoint)
        fuseki.run_sparql(sparql_str=sparql_str)

    # queries
    ###

    def run_sparql(sparql_str, tripple_term="tt") -> list:
        values = list()
        fuseki_query:FusekiQuery = FusekiQuery(KBM.fuseki_base_url, KBM.fuseki_endpoint)

        fuseki_result = fuseki_query.run_sparql(sparql_str)
        bindings = KBM.extract_bindings(fuseki_result)
        if bindings:
            for b in bindings:
                if tripple_term == '*':
                    values.append(b)

                elif tripple_term in b:
                    values.append(b[tripple_term]['value'].replace(KBM.ponto_prefix, ''))

        return values

    def get_entity_comment(entity_name:str) -> str:
        name = KBM.check_name(entity_name)
        sparql_spec = f'ponto:{name} rdfs:comment ?tt'
        sparql_str = KBM.sparql_prefix + """
            SELECT DISTINCT ?tt
            WHERE
            {
                """ + sparql_spec + """
            }
        """

        return KBM.run_sparql(sparql_str)

    def get_entity_class(entity_name:str) -> str:
        name = KBM.check_name(entity_name)
        sparql_spec = f'ponto:{name} rdfs:subClassOf ?tt'
        sparql_str = KBM.sparql_prefix + """
            SELECT ?tt
            WHERE
            {
                """ + sparql_spec + """
            }
        """

        return KBM.run_sparql(sparql_str)

    def get_entity_subclasses(entity_name:str) -> list:
        name = KBM.check_name(entity_name)
        sparql_spec = f'?tt rdfs:subClassOf ponto:{name}'
        sparql_str = KBM.sparql_prefix + """
            SELECT ?tt
            WHERE
            {
                """ + sparql_spec + """
            }
        """

        return KBM.run_sparql(sparql_str)

    def get_all_classes() -> set:
        sparql_str = KBM.sparql_prefix + """
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

        return KBM.run_sparql(sparql_str)

    def get_all_properties() -> set:
        sparql_str = KBM.sparql_prefix + """
            SELECT DISTINCT ?tt
            WHERE
            {
                ?s ?tt ?o .
            }
        """

        return KBM.run_sparql(sparql_str)

    def define_entity(entity_name):
        name = KBM.check_name(entity_name)
        sparql_spec = f'ponto:{name} rdfs:comment ?tt .'
        sparql_str = KBM.sparql_prefix + """
            SELECT ?tt
            WHERE
            {
                """ + sparql_spec + """
            }
        """

        return KBM.run_sparql(sparql_str)

    def get_all_instances() -> set:
        pass
