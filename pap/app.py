import sys

from argparse import ArgumentParser
from flask_compress import Compress

from index import app
from fuseki.kbm import KBM
from fuseki.dataset import DatasetManager

if sys.version_info[0] < 3:
    raise Exception("Python 2.x is not supported. Please upgrade to 3.x")

Compress(app)

# BE entry point
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-pp", "--ponto-url", dest="path_ponto", required=True, 
                        help="specify the local url to the flat ponto turtle file. e.g.: /usr/local/src/POnto/src/flat/POnto.ttl")
    parser.add_argument("-fu", "--fuseki-url", dest="fbu", default="http://127.0.0.1:3030", 
                        help="specify the url to access fuseki-server frontend. e.g.: http://127.0.0.1:3030")

    args = parser.parse_args()

    KBM.fuseki_base_url = args.fbu
    fs = DatasetManager(args.fbu)
    fs.create_ponto_dataset(args.path_ponto)
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=False)
