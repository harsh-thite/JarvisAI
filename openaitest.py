import cohere
from config import apikey

# Initialize the Cohere client with your API key
co = cohere.Client(apikey)

# Define your prompt
prompt = 'Summarize the importance of teamwork.'

# Create a completion request
response = co.generate(
    model='command-r-plus',  # Use a suitable model if 'command-xlarge-20210915' is not available
    prompt=prompt,
    max_tokens=256,
    temperature=0.7,
    p=1.0,  # Equivalent to top_p in OpenAI
    frequency_penalty=0,
    presence_penalty=0
)

# Print the response from Cohere
print(response.generations[0].text)
