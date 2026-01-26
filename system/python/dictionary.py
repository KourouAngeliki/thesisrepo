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

machdict={
    "3D_Printer": "3dPrinter",
    "AGV": "agv", 
    "Automated_Screwdriver" : "autoScrewdriver",
    "Boiler": "boiler", 
    "Carton_Former": "cartonFormer",
    "CMM": "cmm",
    "CNC_Lathe": "cncLathe",
    "CNC_Mill": "cncMill",
    "Compressor": "compressor",
    "Conveyor_Belt": "conveyorBelt",
    "Crane": "crane",
    "Dryer": "dryer",
    "Forklift_Electric": "forkliftElectric",
    "Furnace": "furnace",
    "Grinder": "grinder",
    "Heat_Exchanger": "heatExchanger",
    "Hydraulic_Press": "hydrPress",
    "Industrial_Chiller": "indChiller",
    "Injection_Molder": "injectionMolder",
    "Labeler": "labeler",
    "Laser_Cutter": "laserCutter",
    "Mixer": "mixer",
    "Palletizer": "palletizer",
    "Pick_and_Place": "pickNplace",
    "Press_Brake": "pressBrake",
    "Pump": "pump",
    "Robot_Arm" : "robotArm",
    "Shrink_Wrapper": "shrinkWrapper",
    "Shuttle_System": "shuttleSystem",
    "Vacuum_Packer": "vacuumPacker",
    "Valve_Controller": "valveController",
    "Vision_System": "visionSystem",
    "XRay_Inspector": "xrayInspector"
}


output_folder = "dataset"
#os.makedirs(output_folder, exist_ok=True) if the folder does not exist make it 

#dictionary into dataframe 
map_df = pd.DataFrame(list(dictionary.items()),columns=["CSV_Column_Name", "Ditto_Property_Name"])
obj_df = pd.DataFrame(list(machdict.items()),columns=["Dataset_Name", "Thing_Name"])

#Save inside the dataset folder
map_df.to_csv(os.path.join(output_folder, "dictionary.csv"), index=False)
obj_df.to_csv(os.path.join(output_folder, "machdict.csv"), index=False)
print("📁 Mapping saved to:", os.path.join(output_folder, "dictionary.csv"))
