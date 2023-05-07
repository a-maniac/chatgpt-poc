import openai
import os
from time import time,sleep
import textwrap
import re

openai.api_key = "e20282dfcc514cc2ab4cf15e1722469c"
openai.api_base =  "https://wpb-am.openai.azure.com/" # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
openai.api_type = 'azure'
openai.api_version = '2022-12-01' # this may change in the future

deployment_name='WPB-AM'


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

def save_file(content, filepath):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


def gpt3_completion(prompt, engine= deployment_name, temp=0.6, top_p=1.0, tokens=2000, freq_pen=0.25, pres_pen=0.0, stop=['<<END>>']):
    max_retry = 5
    retry = 0
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop
                )
            text = response['choices'][0]['text'].replace('\n', '').replace(' .', '.').strip()
            text = re.sub('\s+', ' ', text)
            # filename = '%s_gpt3.txt' % time()
            # with open('gpt3_logs/%s' % filename, 'w') as outfile:
            #     outfile.write('PROMPT:\n\n' + prompt + '\n\n==========\n\nRESPONSE:\n\n' + text)
            return text
            #print(text)
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)


if __name__ == '__main__':
    alltext = open_file('C:/Users/ajosh/OneDrive/Desktop/openai/RecursiveSummarizer/input3.txt')
    chunks = textwrap.wrap(alltext, 2000)
    result = list()
    count = 0
    for chunk in chunks:
        count = count + 1
        prompt = open_file('C:/Users/ajosh/OneDrive/Desktop/openai/RecursiveSummarizer/prompt.txt').replace('<<SUMMARY>>', chunk)
        prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
        summary = gpt3_completion(prompt)
        print('\n\n\n', count, 'of', len(chunks), ' - ', summary)
        result.append(summary)
    save_file('\n\n'.join(result), 'output_%s.txt' % time())