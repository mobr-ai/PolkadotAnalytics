from pap.util.Http import Http
from pap.fuseki.kbm import KBM

# mapping a few of the operations listed on fuseki documentation
# see: https://jena.apache.org/documentation/fuseki2/fuseki-server-protocol.html#adding-a-dataset-and-its-services

def create_ponto_dataset(ponto_url:str, fuseki_base_url:str="http://127.0.0.1:3030"):
    """
    Function to create the POnto dataset in the fuseki server if it does not exist, and injects the POnto ontology in it.
    """
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
    http : Http
        the http session to communicate with the fuseki server
    """

    http:Http = None
    fuseki_base_url = ""

    def __init__(self, fuseki_base_url="http://127.0.0.1:3030"):
        """
        Initializes the dataset manager with the fuseki base url and instantiating the http class to communicate with the fuseki server.
        """
        self.fuseki_base_url = fuseki_base_url
        self.http = Http(fuseki_base_url)

    def create_ponto_dataset(self, path_ponto):
        """
        Creates the POnto dataset in the fuseki server if it does not exist, and injects the POnto ontology in it.
        """
        if self.has_dataset("POnto"):
            return

        r = self.create_dataset("POnto")
        if self.has_dataset("POnto"):
            KBM.inject_turtle_file(path_ponto)

        else:
            #TODO: raise an exception here
            print ("creating POnto dataset has failed")
            print (r)

    def get_all_datasets(self):
        """
        Returns all datasets available in the fuseki-server
        """
        endpoint = '/$/datasets'

        return self.http._get(endpoint)

    def create_dataset(self, dataset_name):
        """
        Creates a dataset named dataset_name
        """
        if not self.has_dataset(dataset_name):
            endpoint = '/$/datasets'
            params = {"dbType": "tdb2", "dbName": dataset_name}

            return self.http._post(endpoint, params=params)

        return self.get_dataset_info(dataset_name)

    def has_dataset(self, dataset_name) -> bool:
        """
        Checks if the dataset dataset_name exists in the fuseki-server.
        Returns True if it does and False otherwise.
        """
        di = self.get_dataset_info(dataset_name)
        return di and di["ds.name"] == f"/{dataset_name}"

    def get_dataset_info(self, dataset_name):
        """
        Returns all the information available about the dataset named dataset_name
        """
        endpoint = f'/$/datasets/{dataset_name}'

        return self.http._get(endpoint)

    def delete_dataset(self, dataset_name):
        """
        Deletes the dataset named dataset_name
        """
        endpoint = f'/$/datasets/{dataset_name}'

        return self.http._delete(endpoint)
