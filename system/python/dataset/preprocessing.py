import pandas as pd
import os

output_folder = "individual_machines"
os.makedirs(output_folder, exist_ok=True)

# 1. Load Main Dataset
df = pd.read_csv('factory_sensor_simulator_2040.csv')

# Drop unnecessary columns (Adjust indices as needed)
df_medium = df.drop(df.columns[[0, 2, 3, 10, 11, 12, 14, 15, 16]], axis=1)

# 2. Load Naming Dictionary
name_mapping_df = pd.read_csv('machdict.csv')
name_lookup = dict(zip(name_mapping_df['Dataset_Name'], name_mapping_df['Thing_Name']))

# 3. Create Machine Counts (Statistics)
# We use value_counts() here—it's much faster than manual looping!
machine_counts = df_medium['Machine_Type'].value_counts().reset_index()
machine_counts.columns = ['MachineName', 'Count']
machine_counts.to_csv('machine_counts.csv', index=False)
print(f"✅ Statistics saved to machine_counts.csv. Total unique types: {len(machine_counts)}")

# 4. Save Individual Files with Dictionary Names
for machine_name in df_medium['Machine_Type'].unique():
    # Filter the dataframe for this specific machine type
    machine_df = df_medium[df_medium['Machine_Type'] == machine_name]
    
    # Drop the 'Machine_Type' column so it's not inside the specific CSV
    machine_df = machine_df.drop(columns=['Machine_Type'])

    # Look up the name from your machdict.csv
    mapped_name = name_lookup.get(machine_name, machine_name) 
    
    # Sanitize name for Windows/Linux file systems
    safe_name = str(mapped_name).replace(" ", "_").replace("/", "_")

    # Create full path and Save
    output_path = os.path.join(output_folder, f"{safe_name}.csv")
    machine_df.to_csv(output_path, index=False)
    
    print(f"✅ Saved {output_path} ({len(machine_df)} rows)")

print("\n🚀 All tasks complete!")