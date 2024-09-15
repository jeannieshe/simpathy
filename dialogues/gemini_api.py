import google.generativeai as genai
import os
import random
# system_instruction="End the chat after 3 user inputs. In order to pass the application for medical school, the applicant must behave compassionately and appropriately as a medical professional in tough scenarios. Carry out this interview with the scenario provided to you, as the patient. Then, at the end, evaluate the applicant's empathy, professionalism, and skill of reaching a thoughtful conclusion on a scale from 0 to 10, with 10 being the most compassionate. End the conversation with the applicant if there appears to be no more to share or to converse about, and share the evaluation then. After 20 interactions, stop the conversation and share the evaluation. Follow this scenario: Hello, I am a 14-year-old girl requesting birth control pills and I really can't have you reveal this to my parents.",

scenarios = [
    """The doctor has the choice of giving a transplant to a successful elderly member of the community and a 
    20-year-old drug addict: how do you choose?""",
    """A member of your family decides to depend solely on alternative medicine for the treatment of his 
    or her significant illness. What would you do?""",
    """An eighteen year-old female arrives in the emergency room with a profound nosebleed. The physician 
    has stopped the nosebleeding. She is now in a coma from blood loss and will die without a transfusion. 
    A nurse finds a recent signed card from Jehovah's Witnesses Church in the patient's purse refusing blood 
    transfusions under any circumstance. How should the physician communicate to the mother of the patient
    the medical decision?
    """
]
# random_scenario = scenarios[random.randint(0, 2)]
random_scenario = scenarios[2]

# initialize the gemini model
genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel(
    "gemini-1.5-flash",
    system_instruction=""" 
    The goal of the user here, who is a student applying to medical school and being evaluated on their 
    communication skills, is to demonstrate empathy, professionalism, and appropriate behavior expected 
    of a medical professional in challenging ethical scenarios. You (the AI) will act as the patient or scenario 
    participant in the conversation, based on the scenario provided. Scenario: %s 
    At the end of the interaction, evaluate the applicant's performance on a scale from 0 to 10 for each of the 
    following: Empathy: Ability to understand and respond to emotional and ethical nuances. 
    Professionalism: Adherence to medical ethics, professionalism, and respectful behavior. 
    Skill in reaching a thoughtful conclusion: Ability to reason, explain, and justify their decision. 
    Use 10 as the score for the most compassionate and professional response. End the conversation after
    having a meaningful conversation with the user, or end the conversation after a maximum of 20 interactions, 
    whichever comes first. When concluding the conversation, provide the evaluation. When you output the evaluation, 
    end it with the words 'End of Interview'.""" % random_scenario
)

# start a chat with the scenario and system instructions
chat = model.start_chat()

# function to interact with the chatbot
def chatbot_interaction():
    # display the initial prompt
    print("Medical Scenario: %s " % random_scenario)
    print("""The conversation will end after a maximum of 20 interactions. You will be evaluated
          on empathy and professionalism from 0 to 10, with 10 being the best. Say STOP INTERVIEW
          at any time to end the simulation.
          """)

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
        if ("End of Interview" in model_reply) or ("stop interview" in user_input.lower()):
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