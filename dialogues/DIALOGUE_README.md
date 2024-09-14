# Using a fetch.ai agent for dialogue
Creating an open dialogue chit-chat structure

latest issue: trying to run the two agents locally, but the best way to do it is through the agentverse instead. the ports are busy
updated the ports to use 8002 and 8003. now i can operate open dialogue between the two!

We now have two agents. 
The first agent will be the user with whatever input they would like the respond. It should implement the whisper speech recognition models.

The second agent will be the AI which responds with a preset character's AI response. mimicking the 14 year old girl. It should implement a Google Gemini API