import unittest

from fuseki.dataset import create_ponto_dataset
from index import PONTO_URL
from fuseki.kbm import KBM

def get_test_sparql_spec(entity_name:str) -> str:
    name = KBM.check_name(entity_name)
    sparql_s_spec = f"ponto:{name} ?p ?o ."
    sparql_o_spec = f"?s ?p ponto:{name} ."
    return KBM.sparql_prefix + """
        SELECT *
        WHERE {
        {
            """ + sparql_s_spec + """
        }
        UNION
        {
            """ + sparql_o_spec + """
        }
        }
    """

class KBTestCase(unittest.TestCase):
    def setUp(self):
        create_ponto_dataset(PONTO_URL)

    def test_crud(self):

        # (C) creating with knowledge inject
        KBM.inject_turtle_file("test.ttl")
        sparql_spec = get_test_sparql_spec("MOBRChain")

        print(sparql_spec)

        # (R) reading to check if all the 3 triple were injected
        l = KBM.run_sparql(sparql_spec, "*")
        assert len(l) == 3

        # (U) updating MOBRChain name to MOBRSysChain
        # updating when it appears as a subject and then as an object
        KBM.update_entity("MOBRChain", "MOBRSysChain")
        KBM.update_entity("MOBRChain", "MOBRSysChain", "o")

        # reading to check if
        #   1. there are 3 triples with MOBRSysChain
        #   2. there are 0 triples with MOBRChain

        # this is 1
        sparql_spec = get_test_sparql_spec("MOBRSysChain")
        l = KBM.run_sparql(sparql_spec, "*")
        assert len(l) == 3

        # this is 2
        sparql_spec = get_test_sparql_spec("MOBRChain")
        l = KBM.run_sparql(sparql_spec, "*")
        assert len(l) == 0

        # (D) deleting MOBRSysChain as subject and then as object
        KBM.delete_entity("MOBRSysChain")
        KBM.delete_entity("MOBRSysChain", "o")

        # asserting if it was deleted indeed
        sparql_spec = get_test_sparql_spec("MOBRSysChain")
        l = KBM.run_sparql(sparql_spec, "*")
        assert len(l) == 0

if __name__ == "__main__":
    unittest.main()
