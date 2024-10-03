from openai import OpenAI
from dotenv import load_dotenv
import os
import validators
import json

TEXTMODEL = "gpt-3.5-turbo"
IMGMODEL = "gpt-4o"

#to get startet with the llm model
#create a .env file in the root directory and add the OPENAI_API_KEY
openai_key = ""
load_dotenv()
#automate the process of getting the api key, depending on the system you are running the code
if os.getenv('OPENAI_API_KEY') is None:
    print("Please create a .env file in the root directory and add the OPENAI_API_KEY")
    exit()
else:
    openai_key = os.getenv('OPENAI_API_KEY')

openaiClient = OpenAI(api_key=openai_key)

system = "You are a helpfull asistant, supporting interactions in social situations."

def exampleJson():
    return '{"people": [{"description": "young man with black hair", "emotions": ["happy", "sad"], "possible-interactions": ["greeting", "small-talk", "conversation"]}]}'

def returnJSONAnswerPrompt(originalPrompt : str = None):
    return f"Answer only in JSON format, using the following format {exampleJson()}: {originalPrompt}"

def ragPrompt(prompt : str = None, additionalData = None):
    return f"{prompt} {additionalData}"

def prompt(prompt : str = None, additionalData = None, image : str = None, returnJson : bool = False, returnDict : bool = False):
    returnValue = ""
    messages = [{"role": "system", "content" : system}]
    modelToUse = TEXTMODEL
    prompt = ragPrompt(prompt, additionalData)
    #force it to be a json answer prompt
    prompt = prompt if not returnJson else returnJSONAnswerPrompt(prompt)
    messages.append({"role": "user", "content": [{ 
        "type" : "text", 
        "text" : prompt 
    }]})
    if image is not None:
        if not validators.url(image):
            image = f"data:image/jpeg;base64,{image}"
        messages[1]["content"].append({"type": "image_url", "image_url": { "url" : image}})
        modelToUse = IMGMODEL

    if returnJson:
        returnValue = openaiClient.chat.completions.create(
            model=modelToUse,
            max_tokens= 400,
            response_format={ "type": "json_object" },
            messages=messages,
            temperature=0,
            n=1,
        )
    else :
        returnValue = openaiClient.chat.completions.create(
            model=modelToUse,
            messages=messages,
            temperature=0,
            n=1,
        )
    returnValue = returnValue.choices[0].message.content
    if returnDict:
        return json.loads(returnValue)
    return returnValue