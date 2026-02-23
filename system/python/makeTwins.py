import requests
import pandas as pd
import json
import os
import numpy as np


dictionary = pd.read_csv("dataset/machdict.csv")

for _, data in dictionary.iterrows():
    thingId = f"machine:{data['Thing_Name']}"
    definition = f"fac:{data['Thing_Name']}:0.0.1"
    t = " ".join(data['Dataset_Name'].split('_'))

    arxeio = pd.read_csv(f"dataset/individual_machines/{thingId.split(":")[-1]}.csv")
    row1 = arxeio.iloc[0]
    row1 = row1.where(row1.notna(), None)



    sensors =  {
                    "tempC": 105.2,
                    "vibMms": 20.48,
                    "dB": 56.93,
                    "oilLvlpct": 66.46,
                    "coolLvlpct": 86.63,
                    "kW": 157.37,
                    "aiSuperv": True,
                    "laserIntensity": row1["Laser_Intensity"] ,
                    "hydrPressure": row1["Hydraulic_Pressure_bar"],
                    "coolLvlMin": row1["Coolant_Flow_L_min"],
                    "heatIndex": row1["Heat_Index"],
                    "aiOverrideEvents": 2
                }

    
    prop = {k: v for k, v in sensors.items() if v is not None}
    # print(prop)


    payload = {
        "thingId": thingId,
        "policyId": "factory:mech.Policy",
        "definition": definition,
        "attributes": {
            "type": t
        },

        "features": {
            "sensors": {
                "properties": prop
            }
        }

    }

    headers = {
        "Content-Type": "application/json"
    }


    # r = requests.put(
    #     f"http://localhost:8080/api/2/things/{thingId}",
    #     auth=("ditto", "ditto"),
    #     headers=headers,
    #     json=payload
    # )

    # print(json.dumps(r.json(), indent=2))

    os.makedirs("dataset/twinmodules", exist_ok=True)
    with open(f"dataset/twinmodules/{thingId.split(":")[-1]}.json", "w") as f:
        json.dump(payload, f)

