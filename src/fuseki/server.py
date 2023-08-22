from util.Http import Http
from rdflib import Graph
from pyfuseki import FusekiUpdate

# mapping a few of the operations listed on fuseki documentation
# see: https://jena.apache.org/documentation/fuseki2/fuseki-server-protocol.html#adding-a-dataset-and-its-services

class FusekiServer:
    http:Http = None
    fuseki_base_url = ""

    def __init__(self, fuseki_base_url="http://fuseki:3030"):
        self.fuseki_base_url = fuseki_base_url
        self.http = Http(fuseki_base_url)

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

            fuseki = FusekiUpdate(self.fuseki_base_url, 'POnto')
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
