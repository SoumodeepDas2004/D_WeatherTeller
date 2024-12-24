import requests
import sys
import pandas as pd
import matplotlib.pyplot as plt

location = input("Give your location: ")

def weather(location: str):
    response = requests.request("GET", f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?unitGroup=metric&include=current&key=P9PXD9SUJG6QWY4XZUX3XWTRQ&contentType=json")
    if response.status_code!=200:
        print('Unexpected Status code: ', response.status_code)
        sys.exit() 
    # Parse the JSON response
    jsonData = response.json()

    # Extract only the desired data for the current day
    try:
        current_day_data = jsonData['days'][0] # Access the first day's data
    except KeyError:
        print("Error: 'days' key not found in the JSON response. Check if the location is valid.")
        sys.exit(1)

    desired_keys = {"conditions", "description", "tempmax","tempmin", "humidity", "pressure", "visibility"}
    weather_data = {key: current_day_data.get(key) for key in desired_keys}
    plotdata={"tempmax","tempmin","humidity", "pressure", "visibility"}
    # Create a Pandas DataFrame
    df = pd.DataFrame([weather_data])  # Important: Wrap weather_data in a list

    # Print the DataFrame
    print(f"Weather Data for {location}:\n")
    print(df.T)
    return df
    
df=weather()
desired_keys = {"conditions", "description", "tempmax","tempmin", "humidity", "pressure", "visibility"}
plotdata={"tempmax","tempmin","humidity", "pressure", "visibility"}

# Plotting with Matplotlib
plt.figure(figsize=(10, 6))  # Adjust figure size for better visualization

# Create bar plots for each weather parameter
for i, key in enumerate(plotdata):
    plt.bar(key, df[key][0], label=key)  # df[key][0] gets the value from the DataFrame

plt.xlabel("Weather Parameters")
plt.ylabel("Value")
plt.title(f"Weather Data for {location}")
plt.legend()
plt.tight_layout() # Adjust layout to prevent labels from overlapping
plt.show()
fig, axes = plt.subplots(2, 2, figsize=(10, 8)) 
axes = axes.flatten() 

for i, key in enumerate(desired_keys):
    axes[i].bar(location, df[key][0], label=key)
    axes[i].set_title(key.capitalize())
    axes[i].set_ylabel("Value")

plt.suptitle(f"\n Weather Parameters for : {location}") # Overall title for the subplots
plt.tight_layout(rect=[0, 0, 1, 0.96]) 
plt.show()