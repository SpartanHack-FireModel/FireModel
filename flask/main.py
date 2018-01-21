from flask import Flask, request, send_file
from flask_cors import CORS
import json
import os.path
import sys
sys.path.append('.')
from process import runSimulation

app = Flask(__name__)
CORS(app)
@app.route('/startsimulation',methods=["POST"])
def hello_world():
  args = {'Args' : request.get_json(),
  'Frames' : 2,
  'Subdir' : 'example'
  }
  return json.dumps(args)
@app.route('/test')
def test():
  runSimulation()
  return '1'
  
@app.route('/imgs/<path:sess>/<path:path>')
def imgResp(sess,path):
  sess = sess.replace('..','')
  path = path.replace('..','')
  url = './imgs/' + sess + '/' + path
  print('Looking for',url)
  if(os.path.isfile(url)):
    print('Found')
    return send_file(url,mimetype="image/png")
  else:
    return ''