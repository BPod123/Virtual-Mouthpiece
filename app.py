from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS #comment this on deployment
from api.ApiHandler import ApiHandler

app = Flask(__name__, static_url_path='', static_folder='virtual-mouthpiece/build')
CORS(app) #comment this on deployment
api = Api(app)

@app.route("/", defaults={'path':''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')

api.add_resource(ApiHandler, '/flask/upload')

if __name__ == '__main__':
    app.run(debug=True)