from flask import Flask, request
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)
# Connect to MongoDB
client = MongoClient(host=['mongo:27017'], document_class=dict, tz_aware=False, connect=True)
db = client['mydb']
ip_collection = db['ip']

@app.route('/api/myip')
def get_client_ip():
  
  try:
    client.admin.command('ismaster')
  except:
    return "Server not available"

  #Get client IP address from request
  client_ip = request.remote_addr

  #Check if IP address exists in database
  ip_doc = ip_collection.find_one({'ip': client_ip})

  if ip_doc:
      # Get last request time from database
      last_request_time = ip_doc['last_request_time']
      last_request_time_str = datetime.fromtimestamp(last_request_time).strftime('%a %b %d %H:%M:%S %Z %Y')
      message = f"Your client's IP address is: {client_ip}. Your previous/last request was on {last_request_time_str}."
      current_time = datetime.now().timestamp()
      ip_collection.update_one({'ip': client_ip}, {"$set": {'last_request_time': current_time}})
  else:
      # Record first request time in database''
      current_time = datetime.now().timestamp()
      ip_collection.insert_one({'ip': client_ip, 'last_request_time': current_time})
      message = f"Your client's IP address is: {client_ip}. This is the first message received from your client."
  return message, 200

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)