from util.Http import Http
from rdflib import Graph
from pyfuseki import FusekiUpdate

# mapping a few of the operations listed on fuseki documentation
# see: https://jena.apache.org/documentation/fuseki2/fuseki-server-protocol.html#adding-a-dataset-and-its-services

# FUSEKI_BASE_URL = "http://127.0.0.1:3030"

FUSEKI_BASE_URL = "http://fuseki:3030"

# FUSEKI_BASE_URL = "http://localhost:3030"

class FusekiServer:
    http:Http = None

    def __init__(self):
        self.http = Http(FUSEKI_BASE_URL)

    def create_ponto_dataset(self, path_ponto):
        print ("create_ponto_dataset")
        dsi = self.get_dataset_info("POnto")
        if dsi:
            print ("dataset already exists")
            return

        print ("creating dataset")
        r = self.create_dataset("POnto")
        dsi = self.get_dataset_info("POnto")
        if dsi:
            print ("injecting graph")
            g = Graph()
            g.parse(path_ponto, format='ttl')

            fuseki = FusekiUpdate(FUSEKI_BASE_URL, 'POnto')
            fuseki.insert_graph(g)
            print ("all done")

        else:
            print ("creating failed")
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
