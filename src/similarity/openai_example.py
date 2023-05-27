import openai
import os
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_ORG = os.environ.get("OPENAI_ORG")
openai.organization = OPENAI_ORG
openai.api_key = OPENAI_KEY

prompt = "how hot is the sun?"
model = "text-davinci-003"
response = openai.Completion.create(engine=model, prompt=prompt, max_tokens=20, temperature=0)

generated_text = response.choices[0].text
print(generated_text)
