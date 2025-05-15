from openai import OpenAI
import json

client = OpenAI(api_key="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")

model = "gpt-3.5-turbo-0125"
#model = "gpt-3.5-turbo-0301",

responses_list = []
neutral_resp = []
anthrop_resp = []
ecocen_resp = []
temperatures = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]
for prompt in prompts:
  responses = ""
  for i in range(10):
    response = client.chat.completions.create(
      temperature = temperatures[i],
      #top_p = 1.0,
      model = model,
      max_tokens = 256,
      #response_format={ "type": "json_object" },
      messages = [{"role": "system", "content": prompt}]
    )
    responses += response.choices[0].message.content + "\n"
  responses_list.append(responses)