from openai import OpenAI
from pydantic import BaseModel, Field , ValidationError
from typing import List , Literal, Optional
import instructor
import json 
import os 

class Character(BaseModel):
    name: str
    age: int


class image_labelers(BaseModel):
    defect_label: Literal['Corrosion','Spalling','Deformation','Cracks']
    material: Literal['Concrete','Steel','Wood','Other'] = Field(...,description= "dont be bias for concrete find stiffeners weld or bolt to identify Steel,  and select concrete if you se the rebar or agregates")
    defect_rating : Literal['Minor','Moderate','Major','Extreme'] = Field(...,description= "raiting of the structural defect , do not over estimate it")
    description: Optional[str] = Field(None, description="Succinct description of the image")


# enables `response_model` in create call
client = instructor.patch(
    OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama",  # required, but unused
    ),
    mode=instructor.Mode.JSON,
)

def image_clasifier(image_route:str):
    return client.chat.completions.create(
        model="bakllava:7b-v1-q8_0",
        messages=[
            {
                "role": "user",
                "content": f"identify and label the structural defect base on this image : {image_route}",
            }
        ],
        response_model=image_labelers,
        max_retries = 2,
        temperature=0.1
        
    )


directory_path = r"C:\Users\aleja\Documents\_test_openai_vi\id_test"
results = {}
for filename in os.listdir(directory_path):
    # Check if the file is an image
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif' ,'JPG')):
        # Construct the full file path
        image_path = os.path.join(directory_path, filename)
        
        # Classify the image
        classification_result = image_clasifier(image_path)
        print(classification_result)
        # Construct the new filename with the appended classification
        base, extension = os.path.splitext(filename)

        results[base] = classification_result.dict()

file_name = 'bakllava_7b-v1-q8_0.json'
with open(file_name, 'w') as f:
    json.dump(results, f,indent=4)


