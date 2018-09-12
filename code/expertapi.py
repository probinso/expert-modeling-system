from pathlib import Path
import json
from sys import stderr

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import numpy as np

from atmlibs.modelspec import ProgSpecification
from query import document_interface

#Global varialbes
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Load models as global varialbes

DOCUMENT_TYPE = 'ISA'
DATASTORE = Path('/Users/philipr/git/jpl-playground/code/output')
SPECPATH = Path('/Users/philipr/git/jpl-playground/code/configs/prs.yaml')


def default(o):
    if isinstance(o, np.int64): return str(int(o))
    raise TypeError


@app.route('/PRS/api/v1.0/search', methods=['POST'])
def create_task():
    if not request.json:
        print("DARN")
    data = request.json

    if data['Anomaly_ID']:
        spec = ProgSpecification(SPECPATH)[DOCUMENT_TYPE]
        data = spec.get_document_from_key(int(data['Anomaly_ID']))

    if all(data[key] == '' for key in data):
        retval = []
    else:
        _ = document_interface(SPECPATH, DATASTORE, DOCUMENT_TYPE, data)
        retval = json.loads(_.reset_index().transpose().to_json())

    result = json.dumps(
        {
            'search_results': retval,
            'form': data,
        }, default=default
    )
    print(result, file=stderr)
    return result


## FLASK_APP=./App/simple_api.py FLASK_ENV=development flask run

if __name__ == '__main__':
    app.run(debug=True, port=5000)
