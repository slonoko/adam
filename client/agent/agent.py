from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

root_agent = RemoteA2aAgent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
