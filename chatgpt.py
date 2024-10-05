from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message)


def get_completion(prompt, model="gpt-3.5-turbo"):
  messages = [{"role": "user", "content": prompt}]
  response = openai.chat.completions.create(
    model=model,
    messages=messages,
    temperature=0,  # this is the degree of randomness of the model's output
  )
  return response.choices[0].message["content"]