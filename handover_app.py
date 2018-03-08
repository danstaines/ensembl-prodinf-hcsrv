#!/usr/bin/env python
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import re

from ensembl_prodinf.handover_tasks import handover_database

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('handover_config')
app.config.from_pyfile('handover_config.py')

cors = CORS(app)

# use re to support different charsets
json_pattern = re.compile("application/json")

@app.route('/submit', methods=['POST'])
def handover():
    if json_pattern.match(request.headers['Content-Type']):

        logging.debug("Submitting handover request " + str(request.json))
        spec = request.json

        if 'src_uri' not in spec or 'contact' not in spec or 'type' not in spec or 'comment' not in spec or 'tgt_uri' in spec:
            return "Handover specification incomplete - please specify src_uri, contact, type and comment", 415

        ticket = handover_database(spec)
        logging.info(ticket)
        return jsonify(ticket);
    
    else:
        return "Could not handle input of type " + request.headers['Content-Type'], 415

