import paho.mqtt.client as paho
import socket
import json

port = 1883
topic = "command"
client_id = 100

#connect is a blocking function 
#rc : return code --> used for checking that the connection was established 
def on_connect(client, userdata, flags, rc):
    if(rc == 0):
        client.connected_flag = True
        print("Connection successful, returned code=",rc)
        client.subscribe(topic,2)
        print("Subscribed to:",topic,"with QOS 2")
    else:
        print("Bad connection, Returned code=",rc)

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

def on_message(client,userdata,message):
    print(message.payload)
    json_payload = message.payload
    payload = json.loads(json_payload)
    group_name = payload["group_name"]
    clientId = payload["clientId"]
    if(group_name != "" and clientId != ""):
        client.subscribe(group_name,2)
        print("Created topic and subscribed to:", group_name, clientId)
        msg = {"text": "group created", "to": payload["clientId"], "from": "server", "clientId": client_id, "group_name": group_name }
        payload_msg = json.dumps(msg)
        #client.on_publish = on_publish
        #client.loop_stop()
        #client.loop_start()
        #client.loop()
        client.publish(topic,payload_msg,2)
        #client.loop_start()
        #client.loop_stop()
    else:
        print("Name not specified / group not to be formed")
    

client = paho.Client("server")

#assign function to callbacks:
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
#client.on_subscribe = on_subscribe

client.username_pw_set(username="server",password="irule")
print("Connecting to broker")
client.connect("127.0.0.1",port)
client.loop_start()
#client.loop_stop()
#client.disconnect()
client.loop_forever()
