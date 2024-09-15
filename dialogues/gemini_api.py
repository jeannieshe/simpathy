import google.generativeai as genai
import os

# define system instructions to set the character of the AI (the person in the scenario)
instructions = {
    "behavior": "You are struggling with conflicting thoughts as a young teenage girl and are looking for advice. You are anxious and unsure of yourself."
}

context = "In order to pass the application for medical school, the applicant must behave compassionately and appropriately as a medical professional in tough scenarios. Carry out this interview with the scenario provided to you, as the patient. Then, at the end, evaluate the applicant's empathy, professionalism, and skill of reaching a thoughtful conclusion on a scale from 0 to 10, with 10 being the most compassionate. End the conversation with the applicant after 3 interactions, or if there appears to be no more to share or to converse about, whichever comes first, and share the score evaluation and explanation."

# initialize the gemini model
genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel(
    "gemini-1.5-flash",
    system_instruction="End the chat after 3 user inputs. In order to pass the application for medical school, the applicant must behave compassionately and appropriately as a medical professional in tough scenarios. Carry out this interview with the scenario provided to you, as the patient. Then, at the end, evaluate the applicant's empathy, professionalism, and skill of reaching a thoughtful conclusion on a scale from 0 to 10, with 10 being the most compassionate. End the conversation with the applicant if there appears to be no more to share or to converse about, and share the evaluation then. After 20 interactions, stop the conversation and share the evaluation. Follow this scenario: Hello, I am a 14-year-old girl requesting birth control pills and I really can't have you reveal this to my parents.",
    # context=context
)
# define a specific scenario as content for the conversation
history = [
    # {"role": "system", "parts": ["You are struggling with conflicting thoughts as a young teenage girl and are looking for advice. You are anxious and unsure of yourself."]},
    # {"role": "model", "parts": ["Hello, I am a 14-year-old girl requesting birth control pills and I really can't have you reveal this to my parents."]},
    # {"role": "model", "parts": []}
]

# start a chat with the scenario and system instructions
chat = model.start_chat(
    history=history,
    #system_instruction=instructions,
    #context=context,
    # temperature=0.7,
    # max_tokens=150,
    # top_p=0.9,
    # frequency_penalty=0.5,
    # presence_penalty=0.6
)

# function to interact with the chatbot
def chatbot_interaction():
    # display the initial prompt
    print("Medical Scenario:")
    for exchange in history:
        print(f"{exchange['role'].capitalize()}: {exchange['parts']}")

    # loop for user interaction
    while True:
        user_input = input("You: ") # this is where to add the whisper text interaction
        
        # add user input to chat history
        print(user_input)
        # chat.history.append({"role": "user", "parts": [user_input]})
        print(chat.history)
        
        # generate a response from the model

        # print(user_input, chat.history)

        response = chat.send_message(user_input)
        # print(response.candidates[0].content.parts[0].text)
        model_reply = response.candidates[0].content.parts[0].text

        # add the model's response to the chat history
        print(model_reply)
        # chat.history.append({"role": "model", "parts": [model_reply]})

        # print the model's reply to the terminal
        print(f"Chatbot: {model_reply}") # this is where to add the text to voice

        # exit condition
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting chat...")
            break

# run the chatbot interaction
# chat = model.start_chat(
#     history=[
#         {"role": "user", "parts": "Hello"},
#         {"role": "model", "parts": "Great to meet you. What would you like to know?"},
#     ]
# )

if __name__ == "__main__":
    chatbot_interaction()

# Why don't you feel comfortable talking to your parents?