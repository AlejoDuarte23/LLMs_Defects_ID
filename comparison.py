import json
import os
import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt
# Define the paths to your JSON files
import numpy as np 
json_files = [
r'C:\Users\aleja\Documents\testing_ollama\7b-v1.6-mstrl-q8.json',
r'C:\Users\aleja\Documents\testing_ollama\7b-v1.6-q4.json',
r'C:\Users\aleja\Documents\testing_ollama\13b-v1.5-q2.json',
r'C:\Users\aleja\Documents\testing_ollama\13b-v1.6-vcn-q5.json',
r'C:\Users\aleja\Documents\testing_ollama\gpt-4V.json'
]

def extract_numeric(s):
    match = re.search(r'\d+', s)
    return int(match.group()) if match else 0

def sort_numeric(value):
    numbers = re.findall(r'\d+', value)
    return int(numbers[0]) if numbers else 0



# Load the JSON data
models_data = {}
for file_path in json_files:
    # Correctly remove only the ".json" extension to keep the full model name
    model_name = os.path.basename(file_path)[:-5]  # Removes the last 5 characters, ".json"
    with open(file_path, 'r') as file:
        models_data[model_name] = json.load(file)

# Filter out the images and rename them, excluding "GOPR1630-0001"
common_images = set.intersection(*[set(data.keys()) for data in models_data.values()])
common_images.discard("GOPR1630-0001")  # Remove the specified image

# Rename images and prepare data for comparison
image_mapping = {img: f"Img. {i+1}" for i, img in enumerate(sorted(common_images, key=sort_numeric))}
comparison_data = []

for model, images in models_data.items():
    for image_id, features in images.items():
        if image_id in image_mapping:
            comparison_data.append({
                'Model': model,
                'ImageID': image_mapping[image_id],
                'DefectLabel': features['defect_label'],
                'Material': features['material']
            })

# Convert to DataFrame for easier manipulation
df = pd.DataFrame(comparison_data)


df['MatchScore'] = ((df['DefectLabel'] == 'Corrosion')).astype(int)
# df['MatchScore'] = ((df['DefectLabel'] == 'Corrosion') & (df['Material'] == 'Steel')).astype(int)


pivot_df = df.pivot_table(index='Model', columns='ImageID', values='MatchScore', aggfunc='sum')

sorted_columns = sorted(pivot_df.columns, key=extract_numeric)
pivot_df = pivot_df[sorted_columns]
annotations = np.where(pivot_df.to_numpy() == 1, '100%', '0%')

plt.figure(figsize=(12, 6))
sns.heatmap(pivot_df, annot=annotations, fmt='',    cmap="YlGnBu", cbar=False, linewidths=1, square=True)
# plt.title('Model Comparison Identifiying Defect Type and Material')
plt.title('Model Comparison Identifiying Defect Type Only')
plt.xticks(rotation=45)

plt.show()