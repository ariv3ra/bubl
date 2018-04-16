from __future__ import print_function
from telesign.messaging import MessagingClient

from flask import Flask
import requests
import json
import tweepy

app = Flask(__name__)

#Twitter Creds here
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

total_cap_cm = 10 # Defines the total capacity for container in Centimeters calculated by the distance between the Empty bottom of the container & the Sensor

url = "https://api.microshare.io/share/{Enter recType Here}/tags/latest?details=true" # Microshare.io API enter the recType to poll
headers = {'Authorization':'Bearer {Enter the Microshare Token here}'}  # Microshare.io Authorization Token
telesign_customer_id = ''
telesign_api_key = ''
notif_sent_glob = False

def get_capacity():
    
    resp = requests.get(url, headers=headers).json()
    current_capcity = 0
    print(resp)
    for r in resp['objs']:
        current_capcity = r['data']["payload_fields"]["payload"]
        return current_capcity

def convert_capcity(current_capacity, total_capacity):
    percentile = 100 - ((float(current_capacity) / float(total_capacity)) * 100)
    print("PERCENTILE: ",percentile)
    return percentile


@app.route('/notification')
def get_payload():
    capacity = get_capacity()
    percent_capacity = convert_capcity(capacity, total_cap_cm)
    if (int(percent_capacity) > 75):       
        global notif_sent_glob          # Message sent Flag
        if not notif_sent_glob:
            phone_number = "" # Send text to this Phone number
            message = "The container capacity is at: {0}".format(percent_capacity)
            message_type = "ARN"

            messaging = MessagingClient(telesign_customer_id,telesign_api_key)
            response = messaging.message(phone_number, message, message_type)

            # Send Twitter Update
            tmsg = "Container is {}% Full. Your container service provider has been notified & will respond shortly".format(percent_capacity)
            resp_message = '@{0}\n{1}'.format('', tmsg.encode('utf-8')) # Enter Twitter msg here
            ret = {'msg':'- SMS Alert Sent', 'payload':percent_capacity} # SMS Message
            notif_sent_glob = True
            try:
                api.update_status(resp_message)
            except Exception as e:
                print("ERROR: {0}".format(e.message))
        ret = {'msg':'- SMS Alert Sent', 'payload':percent_capacity}  
    else:
        ret = {'msg':'','payload':percent_capacity}
        notif_sent_glob = False
    return json.dumps([ret])
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)