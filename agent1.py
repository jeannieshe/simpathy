# Import required libraries
import json
 
from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
from dialogues.chitchat import ChitChatDialogue
 
CHAT_AGENT_ADDRESS = "agent1qd5mcvw0y2tkfmk5233gd978894c7ntxzrs8pqqxc57afdqp2uhwv5yumjp" # agent 2 address here
# agent 1 address: agent1qfm5htzy8q7m6l0d4rw0q0wmcuuq0enmxw3l5dvf49g7zzqfshg05khd0ay
 
agent = Agent(
    name="chit_agent",
    seed="secret_seed",
    port=8002,
    endpoint="http://127.0.0.1:8002/submit",
)
 
fund_agent_if_low(agent.wallet.address())
 
# Define dialogue messages; each transition needs a separate message
class InitiateChitChatDialogue(Model):
    pass
 
class AcceptChitChatDialogue(Model):
    pass
 
class ChitChatDialogueMessage(Model):
    text: str
 
class ConcludeChitChatDialogue(Model):
    pass
 
class RejectChitChatDialogue(Model):
    pass
 
# Instantiate the dialogues
chitchat_dialogue = ChitChatDialogue(
    version="0.1",
    agent_address=agent.address,
)
 
# Get an overview of the dialogue structure
print("Dialogue overview:")
print(json.dumps(chitchat_dialogue.get_overview(), indent=4))
print("---")
 
@chitchat_dialogue.on_initiate_session(InitiateChitChatDialogue)
async def start_chitchat(
    ctx: Context,
    sender: str,
    _msg: InitiateChitChatDialogue,
):
    ctx.logger.info(f"Received init message from {sender}")
    # Do something when the dialogue is initiated
    await ctx.send(sender, AcceptChitChatDialogue())
 
@chitchat_dialogue.on_start_dialogue(AcceptChitChatDialogue)
async def accept_chitchat(
    ctx: Context,
    sender: str,
    _msg: AcceptChitChatDialogue,
):
    ctx.logger.info(
        f"session with {sender} was accepted. I'll say 'Hello!' to start the ChitChat"
    )
    # Do something after the dialogue is started; e.g. send a message
    await ctx.send(sender, ChitChatDialogueMessage(text="Hello!"))
 
@chitchat_dialogue.on_reject_session(RejectChitChatDialogue)
async def reject_chitchat(
    ctx: Context,
    sender: str,
    _msg: RejectChitChatDialogue,
):
    # Do something when the dialogue is rejected and nothing has been sent yet
    ctx.logger.info(f"Received reject message from: {sender}")
 
@chitchat_dialogue.on_continue_dialogue(ChitChatDialogueMessage)
async def continue_chitchat(
    ctx: Context,
    sender: str,
    msg: ChitChatDialogueMessage,
):
    # Do something when the dialogue continues
    ctx.logger.info(f"Received message: {msg.text}")
    try:
        my_msg = input("Please enter your message:\n> ")
        if my_msg != "exit":
            await ctx.send(sender, ChitChatDialogueMessage(text=my_msg))
        else:
            await ctx.send(sender, ConcludeChitChatDialogue())
            ctx.logger.info(
                f"Received conclude message from: {sender}; accessing history:"
            )
            ctx.logger.info(chitchat_dialogue.get_conversation(ctx.session))
    except EOFError:
        await ctx.send(sender, ConcludeChitChatDialogue())
 
@chitchat_dialogue.on_end_session(ConcludeChitChatDialogue)
async def conclude_chitchat(
    ctx: Context,
    sender: str,
    _msg: ConcludeChitChatDialogue,
):
    # Do something when the dialogue is concluded after messages have been exchanged
    ctx.logger.info(f"Received conclude message from: {sender}; accessing history:")
    ctx.logger.info(chitchat_dialogue.get_conversation(ctx.session))
 
agent.include(chitchat_dialogue)
 
if __name__ == "__main__":
    print(f"Agent address: {agent.address}")
    agent.run()