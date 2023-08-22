import os, json
from flask import Flask, render_template, jsonify, make_response, send_from_directory
from fuseki.kbm import KBM

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
@app.route('/kbm/getConcepts', methods=['GET'])
def kbm_get_concepts():
    allc = KBM.get_all_classes()
    return reply_list(allc, ok_status_code)

@app.route('/kbm/getProperties', methods=['GET'])
def kbm_get_properties():
    allp = KBM.get_all_properties()
    return reply_list(allp, ok_status_code)

@app.route('/kbm/getParent/<entity_name>', methods=['GET'])
def kbm_get_parent(entity_name:str):
    eclass = KBM.get_entity_class(entity_name)
    return reply_list(eclass, ok_status_code)

@app.route('/kbm/getChildren/<entity_name>', methods=['GET'])
def kbm_get_children(entity_name:str):
    sclasses = KBM.get_entity_subclasses(entity_name)
    return reply_list(sclasses, ok_status_code)

@app.route('/kbm/defineEntity/<entity_name>', methods=['GET'])
def kbm_define_entity(entity_name:str):
    eclass = KBM.define_entity(entity_name)
    return reply_list(eclass, ok_status_code)

@app.route('/kbm/sparql_query/<sparql_spec>/<select_term>', methods=['GET'])
def kbm_sparql_query(sparql_spec:str, select_term:str):
    eclass = KBM.run_sparql(sparql_spec, select_term)
    return reply_list(eclass, ok_status_code)

@app.route('/kbm/knowledge_injection/<turtle_file>', methods=['GET'])
def kbm_knowledge_injection(turtle_file:str):
    eclass = KBM.inject_turtle_file(turtle_file)
    return reply_list(eclass, ok_status_code)
