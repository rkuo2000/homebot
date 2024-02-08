import g4f

# Print all available providers
print([
    provider.__name__
    for provider in g4f.Provider.__providers__
    if provider.working
])
print()

# Execute with a specific provider
response = g4f.ChatCompletion.create(
    model="gpt-3.5-turbo",
    provider=g4f.Provider.Aura, # Bing
    messages=[{"role": "user", "content": "How are you ?"}],
    stream=True,
)

result =""
for message in response:
    result += message
print(result)
