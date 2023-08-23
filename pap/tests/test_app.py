import unittest
from urllib.parse import quote
from werkzeug.datastructures import FileStorage


from fuseki.dataset import create_ponto_dataset
from index import app, PONTO_URL

class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['DEBUG'] = True
        app.config['TESTING'] = True
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        create_ponto_dataset(PONTO_URL)

    def tearDown(self):
        self.ctx.pop()

    def test_home(self):
        response = self.client.get("/")
        html = response.data.decode()

        assert response.status_code == 200
        assert "<!DOCTYPE html>" in html

    def test_swagger(self):
        response = self.client.get("/swagger")
        html = response.data.decode()

        assert response.status_code == 200
        assert "<!DOCTYPE html>" in html

    def test_concepts(self):
        response = self.client.get("/kbm/getConcepts")
        json = response.data.decode()

        assert response.status_code == 200
        assert response.is_json == True
        assert "DistributedLedger" in json

    def test_properties(self):
        response = self.client.get("/kbm/getProperties")
        json = response.data.decode()

        assert response.status_code == 200
        assert response.is_json == True
        assert "hasParachain" in json

    def test_parent(self):
        response = self.client.get("/kbm/getParent/Parachain")
        json = response.data.decode()

        assert response.status_code == 200
        assert response.is_json == True
        assert "DistributedLedger" in json

    def test_children(self):
        response = self.client.get("/kbm/getChildren/DistributedLedger")
        json = response.data.decode()

        assert response.status_code == 200
        assert response.is_json == True
        assert "Parachain" in json

    def test_definition(self):
        response = self.client.get("/kbm/defineEntity/Parachain")
        json = response.data.decode()

        assert response.status_code == 200
        assert response.is_json == True
        assert "blockchain" in json

    def test_sparql_query(self):
        sparql_spec = quote("PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX ponto: <http://www.mobr.ai/ontologies/ponto#> SELECT ?tt WHERE { ponto:Parachain rdfs:comment ?tt . }", safe="")
        response = self.client.get("/kbm/sparql_query/tt/" + sparql_spec)

        json = response.data.decode()

        assert response.status_code == 200
        assert response.is_json == True
        assert "blockchain" in json

    def test_knowledge_injection(self):
        ttl_file = FileStorage(
            stream=open("test.ttl", "rb"),
            filename="test.ttl",
            content_type="text/turtle",
        )

        response = self.client.post(
            "/kbm/knowledge_injection",
            data={"turtle_file": ttl_file},
            content_type='multipart/form-data'
        )

        json = response.data.decode()

        assert response.status_code == 200
        assert response.is_json == True
        assert "injected" in json

if __name__ == "__main__":
    unittest.main()
