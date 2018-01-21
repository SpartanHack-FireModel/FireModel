from flask import Flask, request, send_file, make_response
from flask_cors import CORS
import json
import os.path
import sys
sys.path.append('.')
from process import runSimulation, stepSimulation
from functools import wraps, update_wrapper
from datetime import datetime

game_board = 0
frames = 0
def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
        
    return update_wrapper(no_cache, view)

app = Flask(__name__)
CORS(app)
@app.route('/startsimulation',methods=["POST"])
def hello_world():
  global frames
  global game_board
  req = request.get_json()
  print(req)
  numFrames,gb = runSimulation(req['start'],req['humidity'],req['windSpeed'],req['windDir'])
  frames = numFrames
  game_board = gb
  args = {'Args' : request.get_json(),
  'Frames' : numFrames,
  'Subdir' : 'example'
  }
  return json.dumps(args)
@app.route('/stepsimulation',methods=["POST"])
def step_world():
  global frames
  global game_board
  req = request.get_json()
  print(req)
  numFrames,gb = stepSimulation(game_board,frames,req['humidity'],req['windSpeed'],req['windDir'])
  frames = numFrames
  game_board = gb
  args = {'Args' : request.get_json(),
  'Frames' : numFrames,
  'Subdir' : 'example'
  }
  return json.dumps(args)



@app.route('/test')
def test():
  fp = {
  'x':50,
  'y':60
  }
  runSimulation(fp)
  return '1'
  
@app.route('/imgs/<path:sess>/<path:path>')
@nocache
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