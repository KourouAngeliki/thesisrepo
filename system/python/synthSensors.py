import paho.mqtt.client as mqtt
import pandas as pd
import json
import time
import os


#read the dataset you want to make into a synthetic sensor
df = pd.read_csv("dataset/individual_machines/furnace.csv")
#the dictionary for the .json file mapping
mapping_df = pd.read_csv("dataset/dictionary.csv")
csv_to_ditto_map = dict(zip(mapping_df["CSV_Column_Name"], mapping_df["Ditto_Property_Name"]))

#Establishing mqtt client
mqttc = mqtt.Client(
    client_id="synthsensors",
    protocol=mqtt.MQTTv5
)

mqttc.connect("localhost", 1883)
mqttc.loop_start()


row = df.iloc[49]
properties = {}
for csv_col, ditto_col in csv_to_ditto_map.items():
    if csv_col in row:
        val = row[csv_col]
        if pd.notna(val):
            if hasattr(val, 'item'):
                val = val.item()
            properties[ditto_col] = val

# Correct payload: just the properties
payload = json.dumps(properties)
topic = f"machines/furnace/things/twin/commands/modify"


mqttc.publish(topic, payload, qos=1)
time.sleep(1)
mqttc.disconnect()
mqttc.loop_stop()

print(f"Published to {topic}: {payload}")

#mqttc.publish("machines/furnace/things/twin/commands/modify", json.dumps(test_json), qos=1)
