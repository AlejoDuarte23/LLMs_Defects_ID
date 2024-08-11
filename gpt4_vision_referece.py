from openai import OpenAI
from pydantic import BaseModel, Field,ValidationError
from typing import List , Literal, Optional

import instructor
import json 
import os 
import base64

class Character(BaseModel):
    name: str
    age: int

class image_labelers(BaseModel):
    defect_label: Literal['Corrosion','Spalling','Deformation','Cracks']
    material: Literal['Concrete','Steel','Wood','Other'] = Field(...,description= "dont be bias for concrete find stiffeners weld or bolt to identify Steel,  and select concrete if you se the rebar or agregates")
    defect_rating : Literal['Minor','Moderate','Major','Extreme'] = Field(...,description= "raiting of the structural defect , do not over estimate it")
    description: Optional[str] = Field(None, description="Succinct description of the image")

os.environ["OPENAI_API_KEY"] = ""

def encode_image(image_path: str) -> str:
    """Encode an image to base64."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
client = instructor.patch(OpenAI(),mode=instructor.function_calls.Mode.MD_JSON)

def image_clasifier(image_route:str):
    return client.chat.completions.create(
        # model="llava:7b-v1.6-mistral-q2_K",
        #
        # model="llava:7b-v1.6-mistral-q8_0",
        model="gpt-4-vision-preview",
        messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "identify and label the structural defect base on this image."},
                {"type": "image","image": encode_image(image_route), "resize": 768},
        
            ]}],
        response_model=image_labelers,
        max_retries = 4,
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
        try:
            classification_result = image_clasifier(image_path)
            print(classification_result)
            # Construct the new filename with the appended classification
            base, extension = os.path.splitext(filename)

            results[base] = classification_result.dict()
        except ValidationError as e:
            print(e.errors())

file_name = 'gpt-4-vision-preview.json'
with open(file_name, 'w') as f:
    json.dump(results, f,indent=4)


