import sys

from argparse import ArgumentParser
from flask_compress import Compress

from index import *
from fuseki.server import FusekiServer

if sys.version_info[0] < 3:
    raise Exception("Python 2.x is not supported. Please upgrade to 3.x")

Compress(app)

# BE entry point
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-pp", "--ponto-url", dest="path_ponto", default='',
                        help="specify the local url to the flat ponto turtle file. e.g.: /usr/local/src/POnto/src/flat/POnto.ttl")

    args = parser.parse_args()

    fs = FusekiServer()
    fs.create_ponto_dataset(args.path_ponto)
    app.run(host="0.0.0.0", port=80, debug=False, threaded=False)
