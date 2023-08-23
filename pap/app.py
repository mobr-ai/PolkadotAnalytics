import sys

from argparse import ArgumentParser
from flask_compress import Compress

from index import app, PONTO_URL
from fuseki.dataset import create_ponto_dataset

if sys.version_info[0] < 3:
    raise Exception("Python 2.x is not supported. Please upgrade to 3.x")

Compress(app)

# BE entry point
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-fu", "--fuseki-url", dest="fbu", default="http://127.0.0.1:3030", 
                        help="specify the url to access fuseki-server frontend. e.g.: http://127.0.0.1:3030")

    args = parser.parse_args()

    create_ponto_dataset(PONTO_URL, args.fbu)
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=False)
