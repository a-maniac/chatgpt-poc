import os
import requests
import json
import openai

openai.api_key = "e20282dfcc514cc2ab4cf15e1722469c"
openai.api_base =  "https://wpb-am.openai.azure.com/" # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
openai.api_type = 'azure'
openai.api_version = '2022-12-01' # this may change in the future

deployment_name='WPB-AM' #This will correspond to the custom name you chose for your deployment when you deployed a model. 

# Send a completion call to generate an answer
print('Sending a test completion job')
start_phrase = 'Summarize the content in the following link "https://www.hul.co.in/files/92ui5egz/production/8a1b3f103408328781a6ebf434b8e5172e4bfc91.pdf" in 4000 words'
response = openai.Completion.create(engine=deployment_name, prompt=start_phrase, max_tokens=2000)
text = response['choices'][0]['text'].replace('\n', '').replace(' .', '.').strip()
print(start_phrase+text)