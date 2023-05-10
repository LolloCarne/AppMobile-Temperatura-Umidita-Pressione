import json
import random
from typing import get_args
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import datetime


app= Flask(__name__)
api=Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:banana.33@localhost:3306/iot'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Dato(db.Model):
    __tablename__='dati'
    id=db.Column(db.Integer, primary_key=True,autoincrement=True)
    temperatura=db.Column(db.String(10),nullable=False)
    umidità=db.Column(db.String(10),nullable = False)
    pressione=db.Column(db.String(10),nullable=False)
    tempo=db.Column(db.DateTime)
    

resoursce_field={
    'id': fields.Integer,
    'temperatura': fields.String,
    'umidità':fields.String,
    'pressione': fields.String,
    'tempo': fields.DateTime
    }




class UpdateDati(Resource):
    @marshal_with(resoursce_field)
    def get(self):
        last=Dato.query.all()[-1]
        return last

class HandlerDati(Resource):
    @marshal_with(resoursce_field)
    def get(self):
        items=Dato.query.all()
        last10=items[-10:]
        last10.reverse()
        return last10
        
        

    
    def put(self):
        args=put_args.parse_args()
        now=datetime.datetime.now()
        if args['id']:
            dato=Dato(id=args['id'],temperatura=args['temp'],umidità=args['hum'],pressione=args['press'],tempo=now)
        else:
            
            dato=Dato(temperatura=args['temp'],umidità=args['hum'],pressione=args['press'],tempo=now)
        db.session.add(dato)
        db.session.commit()
        
        return  200

put_args=reqparse.RequestParser()
put_args.add_argument('id',type=int,required=False)
put_args.add_argument('temp',type=str,required=True)
put_args.add_argument('hum',type=str,required=True)
put_args.add_argument('press',type=str,required=True)
api.add_resource(HandlerDati,'/')
api.add_resource(UpdateDati,'/update')






if __name__ == '__main__':
	app.run(host='192.168.114.157', port=8000,debug = True)