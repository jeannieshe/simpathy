import google.generativeai as genai
import os
import random

# initialize all scenarios
scenarios = [
    """The doctor has the choice of giving a transplant to a successful elderly member of the community and a 
    20-year-old drug addict: how do you choose? Explain your answer to the nurse.""",
    """A member of your family decides to depend solely on alternative medicine for the treatment of his 
    or her significant illness. What would you recommend to her? Explain your answer to her.""",
    """An eighteen year-old female arrives in the emergency room with a profound nosebleed. The physician 
    has stopped the nosebleeding. She is now in a coma from blood loss and will die without a transfusion. 
    A nurse finds a recent signed card from Jehovah's Witnesses Church in the patient's purse refusing blood 
    transfusions under any circumstance. How should you communicate to the mother of the patient
    the medical decision?""",
    """Your aunt sits you down and asks you to help with a major family decision. Your maternal grandfather 
    is 70 years old and has been diagnosed with a condition that will kill him some time in the next five 
    years. He can have a procedure that will correct the disease and not leave him with any long-term 
    problems, but the procedure has a 10% mortality rate. He wants to have the procedure, but your aunt 
    does not want him to. How would you talk to your aunt and mediate this issue?""",
    """A patient with Downs Syndrome became pregnant. The patient does not want an abortion. Her mother 
    and husband want the patient to have an abortion. What would you tell the patient?""",
    """A 12-year old boy is diagnosed with a terminal illness. He asked the doctor 
    about his prognosis. His parents requested the doctor not to tell him the bad news. What would you
    tell the mother in this situation?""",
    """A couple has decided to have a child through artificial insemination. They asked you, the physician 
    for sex selection of the child. What should you advise in this situation to the woman?""",
    """A 38-year old schizophrenic patient needs hernia repair. You, the surgeon, are trying to communicate
    the procedure to her. Will you be able to acquire her consent?""",
    """An 18-year old woman is diagnosed to have suspected bacterial meningitis. She refuses therapy and 
    returns to the college dormitory. What should you, a physician, do in this situation?""",
    """You are the emergency doctor on duty when two patients are rushed in within 7 seconds of each other
      and both desperately need a heart transplant. You only have one donor organ available. And both 
      patients are a match and both are equally medically fit for the operation. One patient is a 35-year 
      old single dad with 3 children, while the other is a 35-year-old single male, who’s an Olympic Gold 
      medalist. Who would you give the heart to and why?""",
]
random_scenario = scenarios[random.randint(0, 9)]
# random_scenario = scenarios[2]

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
if __name__ == "__main__":
    chatbot_interaction()