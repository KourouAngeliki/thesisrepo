import pandas as pd
import os

output_folder = "individual_machines"
os.makedirs(output_folder, exist_ok=True)

#pd.read_csv('factory_sensor_simulator_2040.csv')
df = pd.read_csv('factory_sensor_simulator_2040.csv')
df_medium = df.drop(df.columns[[0, 2, 3, 10, 11, 12, 14, 15, 16]], axis=1)


# Get the first column (machine names)
machine_column = df_medium.iloc[:, 0]
overall_count = 0
machine_dict = {} #create dictionary

# Loop through all rows
for machine_type in machine_column:
    if machine_type in machine_dict:
        machine_dict[machine_type] += 1
    else:
        overall_count += 1
        machine_dict[machine_type] = 1

# Convert the dictionary into a DataFrame (table)
machine_table = pd.DataFrame(list(machine_dict.items()), columns=['MachineName', 'Count'])
machine_table.sort_values(by='Count', ascending=False, inplace=True) #descending order
machine_table.to_csv('machine_counts.csv', index=False) 
#machine_table.to_csv(os.path.join(output_folder, 'machine_counts.csv'),index=False)

#print(f"Total unique machines: {overall_count}")
# Assuming df and machine_dict already exist
# df = your original dataframe
# machine_dict = dictionary with machine names as keys


for machine_name in df_medium['Machine_Type'].unique():
    # Filter the dataframe for this machine
    machine_df = df_medium[df_medium['Machine_Type'] == machine_name]
    # Drop the first column (by index)
    machine_df = machine_df.drop(machine_df.columns[0], axis=1)
    # Clean the name for safe filenames
    safe_name = str(machine_name).replace(" ", "_").replace("/", "_")
    # Create full path
    output_path = os.path.join(output_folder, f"{safe_name}.csv")
    # Save file
    machine_df.to_csv(output_path, index=False)
    print(f"✅ Saved {output_path} ({len(machine_df)} rows)")

