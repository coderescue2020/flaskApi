from flask import Flask
from flask import request
import pymongo
from pymongo import MongoClient
from datetime import datetime
import json
from flask import jsonify
app = Flask(__name__)

@app.route('/')
def hello_world():
   client = MongoClient('mongodb+srv://coderescue:sih2020@trycluster-rfees.mongodb.net/test?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE' , ssl = True)
   args = request.args
   disaster_id = ""
   remarks = ""
   latitude = ""
   longitude = ""
   count_of_people = ""
   data = {}
   if ( len(args.getlist('disaster_id')) > 0 ):
   	disaster_id = args.getlist('disaster_id')[0]
   	data["disaster_id"] = disaster_id
   if ( len(args.getlist('remarks')) > 0 ):
   	remarks = args.getlist('remarks')[0]
   	data["remarks"] = remarks
   if ( len(args.getlist('latitude')) > 0 ):
   	latitude = args.getlist('latitude')[0]
   	data["latitude"] = latitude
   if ( len(args.getlist('longitude')) > 0 ):
   	longitude = args.getlist('longitude')[0]
   	data["longitude"] = longitude
   if ( len(args.getlist('count_of_people')) > 0 ):
   	count_of_people = args.getlist('count_of_people')[0]
   	data["count_of_people"] = count_of_people
   if latitude == '' or longitude == '' or disaster_id == '':
   	return jsonify({"status": "Some parameters missing"}), 400
   data["isactive"]=1
   db = client.main.victimsneedhelp
   info = list(db.find({"disaster_id":disaster_id}))
   if( len(info) > 0 ):
   		list_of_victims = info[0]['victims']
   		print(list_of_victims)
   		list_of_victims.insert(0, data)
   		print(list_of_victims)
   		db.replace_one({'disaster_id':disaster_id},{
     		'disaster_id':disaster_id,
     		'victims':list_of_victims
    	})
   else:
   		list_of_victims = []
   		list_of_victims.insert(0 , data)
   		db.insert_one({
     		'disaster_id':disaster_id,
     		'victims':list_of_victims
    	})
    	
   return jsonify({"status": "Added successfully"}), 200

if __name__ == '__main__':
   app.run(debug=True, use_reloader=False)


