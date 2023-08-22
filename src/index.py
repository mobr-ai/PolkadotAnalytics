import os, json
from flask import Flask, render_template, jsonify, make_response, send_from_directory
from fuseki.ponto import Ponto


ok_status_code = 200

app = Flask(__name__)

def reply_list(resp_list:list, status_code:int):
    str_res = json.dumps(resp_list)
    return make_response(jsonify(str_res), status_code)

### FE entry point ###
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('swagger_ui.html')

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), './img/favicon.ico', mimetype='image/vnd.microsoft.icon')


### swagger ###
@app.route('/swagger')
def swagger_ui():
    return render_template('swagger_ui.html')

@app.route('/s_file')
def get_spec():
    return send_from_directory(app.root_path, 'swagger.yml')


### POnto ###
@app.route('/ponto/getConcepts', methods=['GET'])
def ponto_get_concepts():
    allc = Ponto.get_all_classes()
    return reply_list(allc, ok_status_code)

@app.route('/ponto/getProperties', methods=['GET'])
def ponto_get_properties():
    allp = Ponto.get_all_properties()
    return reply_list(allp, ok_status_code)

@app.route('/ponto/getParent/<entity_name>', methods=['GET'])
def ponto_get_parent(entity_name:str):
    eclass = Ponto.get_entity_class(entity_name)
    return reply_list(eclass, ok_status_code)

@app.route('/ponto/getChildren/<entity_name>', methods=['GET'])
def ponto_get_children(entity_name:str):
    sclasses = Ponto.get_entity_subclasses(entity_name)
    return reply_list(sclasses, ok_status_code)

@app.route('/ponto/defineEntity/<entity_name>', methods=['GET'])
def ponto_define_entity(entity_name:str):
    eclass = Ponto.define_entity(entity_name)
    return reply_list(eclass, ok_status_code)
