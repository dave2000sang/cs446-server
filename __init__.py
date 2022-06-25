from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class Word(Resource):
    def get(self)

class Audio(Resource):
    def get(self, word)

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
