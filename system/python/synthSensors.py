import paho.mqtt.client as mqtt
import pandas as pd
import json
import time
import os



#read the dataset you want to make into a synthetic sensor
df = pd.read_csv("dataset/individual_machines/furnace.csv")
mapping_df = pd.read_csv("dataset/dictionary.csv") #the dictionary for the .json file mapping
csv_to_ditto_map = dict(zip(mapping_df["CSV_Column_Name"], mapping_df["Ditto_Property_Name"]))


#Establishing mqtt client
mqttc = mqtt.Client(client_id="mqttcli", protocol=mqtt.MQTTv5)
mqttc.connect("localhost", 1883) #if its not working try localhost or this "127.0.0.1"
mqttc.loop_start()


props = mqtt.Properties(mqtt.PacketTypes.PUBLISH)
props.UserProperty = [("content-type", "application/vnd.eclipse.ditto+json")]



for index, row in df.iterrows():
    # Build the 'value' dictionary dynamically for this specific row
    sensors_value = {}
    
    for csv_col, ditto_col in csv_to_ditto_map.items():
        if csv_col in row:
            val = row[csv_col]
            if pd.notna(val):
                # Convert numpy types to native Python types for JSON serialization
                if hasattr(val, 'item'):
                    val = val.item()
                sensors_value[ditto_col] = val

    # Construct the full Ditto Protocol message
    payload_base = {
        "topic": "machines/furnace/things/twin/commands/modify", 
        "path": "/features/sensors/properties",
        "value": sensors_value
    }

    print(payload_base)

    payload = json.dumps(payload_base)
    topic = "testtopic/machines/furnace/things/twin/commands/modify"

    # Publish mqttc.publish(topic, payload, qos=1)
    mqttc.publish(topic, payload, qos=1, properties=props)
    print(f"Row {index} published to {topic}")
    time.sleep(2)

# Clean shutdown
mqttc.loop_stop()
mqttc.disconnect()
print(f"Finished publishing all rows.")
