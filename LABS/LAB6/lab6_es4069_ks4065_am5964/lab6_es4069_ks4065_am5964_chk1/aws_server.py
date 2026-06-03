from flask import Flask, render_template
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import json
from pymongo import MongoClient, GEO2D

app= Flask(__name__)

app.config['MONGO_DBNAME']= 'coordinates'
app.config['MONGO_URI']= 'mongodb://localhost:27017/coordinates'
mongo= PyMongo(app)
lis = []
@app.route('/post', methods=['POST'])
def add_coordinate():   
    xcoordinate=0
    ycoordinate=0
    zcoordinate=0
    coordinate= mongo.db.coordinates
    xcoordinate= request.json["xcoordinate"]
    ycoordinate= request.json["ycoordinate"]
    zcoordinate= request.json["zcoordinate"]
    print(xcoordinate)
    # coordinate.insert_one({'xcoordinate': xcoordinate, 'ycoordinate': ycoordinate, 'zcoordinate': zcoordinate})
    lis.append({'xcoordinate': xcoordinate, 'ycoordinate': ycoordinate, 'zcoordinate': zcoordinate})
    # new_coordinate=coordinate.find_one({'xcoordinate': xcoordinate} and {'ycoordinate':ycoordinate} and {'zcoordinate':zcoordinate})
    output = {'xcoordinate': xcoordinate,'ycoordinate':ycoordinate, 'zcoordinate':zcoordinate}                 
    return jsonify({'result':output})


@app.route('/get', methods=['GET'])
def get_coordinate():
    global lis
    # coordinate= mongo.db.coordinates
    output= []
    # for c in coordinate.find():
    #     output.append({'xcoordinate': c['xcoordinate'], 'ycoordinate': c['ycoordinate'], 'zcoordinate': c['zcoordinate']})
    for c in lis:
        output.append({'xcoordinate': c['xcoordinate'], 'ycoordinate': c['ycoordinate'], 'zcoordinate': c['zcoordinate']})

    return jsonify({'result' : output})


if __name__== '__main__':
    app.run(debug=True, host="0.0.0.0", port= 5000)
