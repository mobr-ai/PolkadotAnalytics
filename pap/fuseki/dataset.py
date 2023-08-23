from util.Http import Http
from fuseki.kbm import KBM

# mapping a few of the operations listed on fuseki documentation
# see: https://jena.apache.org/documentation/fuseki2/fuseki-server-protocol.html#adding-a-dataset-and-its-services

def create_ponto_dataset(ponto_url:str, fuseki_base_url:str="http://127.0.0.1:3030"):
    KBM.fuseki_base_url = fuseki_base_url
    dm = DatasetManager(fuseki_base_url)
    dm.create_ponto_dataset(ponto_url)

class DatasetManager:
    """
    Fuseki Server Class

    Main goal of this class is to abstract the fuseki server funcionalities like creating an RDF dataset
    or injecting a turtle file in an existent dataset.

    ...

    Attributes
    ----------
    fuseki_base_url : str
        the url to access the fuseki server endpoints
    """

    http:Http = None
    fuseki_base_url = ""

    def __init__(self, fuseki_base_url="http://127.0.0.1:3030"):
        self.fuseki_base_url = fuseki_base_url
        self.http = Http(fuseki_base_url)

    def create_ponto_dataset(self, path_ponto):
        dsi = self.get_dataset_info("POnto")
        if dsi:
            return

        r = self.create_dataset("POnto")
        dsi = self.get_dataset_info("POnto")
        if dsi:
            KBM.inject_turtle_file(path_ponto)

        else:
            print ("creating POnto dataset has failed")
            print (r)

    def get_all_datasets(self):
        endpoint = '/$/datasets'

        return self.http._get(endpoint)

    def create_dataset(self, dataset_name):
        endpoint = '/$/datasets'
        params = {"dbType": "tdb2", "dbName": dataset_name}

        return self.http._post(endpoint, params=params)

    def get_dataset_info(self, dataset_name):
        endpoint = f'/$/datasets/{dataset_name}'

        return self.http._get(endpoint)

    def delete_dataset(self, dataset_name):
        endpoint = f'/$/datasets/{dataset_name}'

        return self.http._delete(endpoint)
