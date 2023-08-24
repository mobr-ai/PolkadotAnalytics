import os
from flask import Flask, render_template, jsonify, send_from_directory, request
from urllib.parse import unquote
from werkzeug.utils import secure_filename

from pap.fuseki.kbm import KBM

app:Flask = Flask(__name__)
"""
Detailed documentation on the flask routes are specified in the swagger UI documentation.

Check http://127.0.0.1/swagger for details.
"""

PONTO_URL = "https://raw.githubusercontent.com/mobr-ai/ponto/main/src/flat/POnto.ttl"


### FE entry point ###
@app.route('/', methods=['POST', 'GET'])
def index():
    """
    platform frontend endpoint
    """
    return render_template('swagger_ui.html')

@app.route('/favicon.ico') 
def favicon(): 
    """
    favicon endpoint
    """
    return send_from_directory(os.path.join(app.root_path, 'static'), './img/favicon.ico', mimetype='image/vnd.microsoft.icon')


### swagger ###
@app.route('/swagger')
def swagger_ui():
    """
    endpoint for the swagger documentation UI
    """
    return render_template('swagger_ui.html')

@app.route('/s_file')
def get_spec():
    """
    access to swagger.yml file
    """
    return send_from_directory(app.root_path, 'swagger.yml')


### POnto ###
@app.route('/kbm/getConcepts', methods=['GET'])
def kbm_get_concepts():
    """
    endpoint to get all concepts described in the POnto dataset
    """
    allc = KBM.get_all_classes()
    return jsonify(allc)

@app.route('/kbm/getProperties', methods=['GET'])
def kbm_get_properties():
    """
    endpoint to get all properties described in the POnto dataset
    """
    allp = KBM.get_all_properties()
    return jsonify(allp)

@app.route('/kbm/getParent/<entity_name>', methods=['GET'])
def kbm_get_parent(entity_name:str):
    """
    endpoint to get the class of an entity named entity_name
    """
    eclass = KBM.get_entity_class(entity_name)
    return jsonify(eclass)

@app.route('/kbm/getChildren/<entity_name>', methods=['GET'])
def kbm_get_children(entity_name:str):
    """
    endpoint to get the subclasses of a class named entity_name
    """
    sclasses = KBM.get_entity_subclasses(entity_name)
    return jsonify(sclasses)

@app.route('/kbm/defineEntity/<entity_name>', methods=['GET'])
def kbm_define_entity(entity_name:str):
    """
    endpoint to get the definition of an entity named entity_name
    """
    eclass = KBM.define_entity(entity_name)
    return jsonify(eclass)

@app.route('/kbm/sparql_query/<select_term>/<path:sparql_spec>', methods=['GET'])
def kbm_sparql_query(select_term, sparql_spec):
    """
    endpoint to run the sparql query specified in sparql_str, returning all the results where
    the term tripple_term appears.
    """
    eclass = KBM.run_sparql(sparql_str=unquote(sparql_spec), tripple_term=select_term)
    return jsonify(eclass)

@app.route('/kbm/knowledge_injection', methods=['POST'])
def kbm_knowledge_injection():
    """
    endpoint to inject a turtle file in the POnto dataset
    """
    file = request.files['turtle_file']
    filename = secure_filename(file.filename)
    file.save(filename)

    KBM.inject_turtle_file(filename)
    return jsonify("knowledge injected")
