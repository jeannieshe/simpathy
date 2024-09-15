import google.generativeai as genai
import os
# system_instruction="End the chat after 3 user inputs. In order to pass the application for medical school, the applicant must behave compassionately and appropriately as a medical professional in tough scenarios. Carry out this interview with the scenario provided to you, as the patient. Then, at the end, evaluate the applicant's empathy, professionalism, and skill of reaching a thoughtful conclusion on a scale from 0 to 10, with 10 being the most compassionate. End the conversation with the applicant if there appears to be no more to share or to converse about, and share the evaluation then. After 20 interactions, stop the conversation and share the evaluation. Follow this scenario: Hello, I am a 14-year-old girl requesting birth control pills and I really can't have you reveal this to my parents.",

# initialize the gemini model
genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel(
    "gemini-1.5-flash",
    system_instruction="Limit the chat to 3 user inputs in total. The goal of the applicant is to demonstrate empathy, professionalism, and appropriate behavior expected of a medical professional in challenging ethical scenarios. You (the AI) will act as the patient or scenario participant in the conversation, based on the scenario provided. Scenario: You have the choice of giving a transplant to a successful elderly member of the community and a 20-year-old drug addict: how do you choose? At the end of the interaction, evaluate the applicant's performance on a scale from 0 to 10 for each of the following: Empathy: Ability to understand and respond to emotional and ethical nuances. Professionalism: Adherence to medical ethics, professionalism, and respectful behavior. Skill in reaching a thoughtful conclusion: Ability to reason, explain, and justify their decision. Use 10 as the score for the most compassionate and professional response. If there appears to be no more to share or discuss before the 3-user-input limit, conclude the conversation early and provide the evaluation."
)

# start a chat with the scenario and system instructions
chat = model.start_chat()

# function to interact with the chatbot
def chatbot_interaction():
    # display the initial prompt
    print("Medical Scenario: ")

    # loop for user interaction
    while True:
        user_input = input("You: ") # this is where to add the whisper text interaction
        
        # add user input to chat history
        chat.history.append({"role": "user", "parts": [user_input]})
        
        # generate a response from the model
        response = chat.send_message(user_input)
        model_reply = response.candidates[0].content.parts[0].text

        # add the model's response to the chat history
        chat.history.append({"role": "model", "parts": [model_reply]})

        # print the model's reply to the terminal
        print(f"Patient: {model_reply}") # this is where to add the text to voice

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