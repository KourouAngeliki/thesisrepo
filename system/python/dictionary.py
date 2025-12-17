import pandas as pd
import os 

dictionary = {
    "Temperature_C": "tempC",
    "Vibration_mms": "vibMms",
    "Sound_dB": "dB",
    "Oil_Level_pct": "oilLvlpct",
    "Coolant_Level_pct": "coolLvlpct",
    "Power_Consumption_kW": "kW",
    "AI_Supervision": "aiSuperv",
    "Laser_Intensity": "laserIntensity",
    "Hydraulic_Pressure_bar": "hydrPressure",
    "Coolant_Flow_L_min": "coolLvlMin",
    "Heat_Index": "heatIndex",
    "AI_Override_Events": "aiOverrideEvents"
}


output_folder = "dataset"
#os.makedirs(output_folder, exist_ok=True) if the folder does not exist make it 

#dictionary into dataframe 
map_df = pd.DataFrame(list(dictionary.items()),columns=["CSV_Column_Name", "Ditto_Property_Name"])

#Save inside the dataset folder
map_df.to_csv(os.path.join(output_folder, "dictionary.csv"), index=False)

print("📁 Mapping saved to:", os.path.join(output_folder, "dictionary.csv"))
