import unittest

from pap.fuseki.dataset import DatasetManager

class DatasetTestCase(unittest.TestCase):
    """
    Testing Dataset CRD operations
    """

    def setUp(self):
        self.dm = DatasetManager()

    def test_crd(self):
        # (C) creating a test dataset
        self.dm.create_dataset("test")

        # (R) reading the server to see if the test dataset was created
        assert self.dm.has_dataset("test")

        # (D) deleting the dataset
        self.dm.delete_dataset("test")
        assert not self.dm.has_dataset("test")

if __name__ == "__main__":
    unittest.main()
