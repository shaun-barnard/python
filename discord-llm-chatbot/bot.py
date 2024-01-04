import asyncio
import datetime
import discord
from dotenv import load_dotenv
from discord.ext import commands
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import GPT4All
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
import os
import sys
import threading

#Configuration
MODEL_PATH = "mistral-7b-v0.1.Q4_K_M.gguf"
BOT_PREFIX_ON = True
BOT_PREFIX = '/b'
BOT_CHANNEL_MESSAGE_ON = True
BOT_CHANNEL_MESSAGE = "Hey guys! Use '/b' followed by your message to interact with me ;)"

#Set Model path
model_path = (MODEL_PATH)

#Set callback handler, stream only the final output of the agent.
callbacks = [StreamingStdOutCallbackHandler()]

#Instantiate a GPT4All language model, specifies the callback handlers, enable verbose output
llm = GPT4All(model=model_path, callbacks=callbacks, verbose=False)

#Set conversation history and context
memory = ConversationBufferWindowMemory(k=24)

#Instatiate conversation chain, pass llm and conversational memory to be employed.
conversation = ConversationChain(llm=llm, memory=memory)

#Set template
template = """Please act as a teenage gamer who is an expert in minecraft, fornite, and other popular games. Feel free to use slang. Try to very subtly keep the conversation going. Your character is like an older brother who is encouraging and uplifting. Stay on topic. Provide answers to questions in a short concise way. Don't talk about the user in the third person. Don't repeat phrases you have already said prior in the conversation. Keep the converstation between you and the user. Username: {username} said the following: {question}"""

#Instatiate prompt template
prompt = PromptTemplate(template=template, input_variables=["username", "question"])

#Instatiate LLMChain to format the prompt template using the input key and the associated language model for text generation
llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=False)

#Load environment variables from a .env
load_dotenv()

#Set toekn from .env
API_TOKEN = os.getenv("API_KEY")

#Discord API to subscribe to all available intents, allowing the bot to receive a wide range of events.
intents = discord.Intents.all()

#creates a bot instance with a command prefix of '!' and pass the intents to be used
bot = commands.Bot(command_prefix='!', intents=intents)

#Define an event handler for the bot's "on_ready" event, which is triggered when the bot has established a connection to the Discord server and is ready to start receiving events. An asynchronous function will be called when the event occurs.
@bot.event
async def on_ready():
    print(f'[+] {bot.user.name} has connected to Discord @ {datetime.datetime.now().replace(microsecond=0)}')   
    for guild in bot.guilds:
        for channel in guild.text_channels:
            #Maxmium number of messages to retrieve from channel history, adjust as needed [SHIT NEEDS FIXING] it's only returning 1 line of chat history
            async for msg in channel.history(limit=None):
                if BOT_CHANNEL_MESSAGE_ON is True:
                    print(f'[+] Bot Channel Message is ENABLED')
                    #If identical BOT_CHANNEL_MESSAGE is already present in channel history, skip sending it to avoid annoying everyone
                    if msg.content == BOT_CHANNEL_MESSAGE:
                        print(f'[-] Identical Bot Channel Message already detected in channel history. Not re-sending.')
                        break
                    else:
                        await channel.send(BOT_CHANNEL_MESSAGE)
                        print(f'[+] Bot Channel Message sent to chat @ {datetime.datetime.now().replace(microsecond=0)}')
                        break
                else:
                    print(f'[+] Bot Channel Message is DISABLED')
            if(BOT_PREFIX_ON) is True:
                print(f'[+] Bot Prefix is ENABLED')
                print(f'[+] {bot.user.name} will only respond to messages starting with "{BOT_PREFIX}"')
            else:
                print("[-] Bot Prefix is DISABLED")
                print(f'[+] {bot.user.name} will respond to all messages in {channel.name}')
            print(f'[+] {bot.user.name} is now monitoring #{channel.name} on "{guild.name}" @ {datetime.datetime.now().replace(microsecond=0)}')
            print("-----------------------------------------------------------------------------------------------------------------------")

#Define an event handler for the bot's "on_message" event, which is triggered when a message is sent on channel which bot it connected to.
@bot.event
async def on_message(message):

    #Retrieve username from message
    username = message.author.name

    #Print message content along with the author's name to console
    print(username + ": " + message.content + " @", message.created_at)

    #Format the prompt with the username and the user's question
    input_text = prompt.format(username=username, question=message.content)

    #Setup string which includes the username and message content, and prepare it for further processing
    #input_text = "###USER:"+username+":###MESSAGE:"+message.content+"\n"

    #Set desired chunk size
    input_chunk_size = 1500
    output_chunk_size = 1500

    #Chunk the input text
    input_chunks = [input_text[i:i + input_chunk_size] for i in range(0, len(input_text), input_chunk_size)]

    #Store the original standard output
    original_stdout = sys.stdout
    #Redirect the standard output to a null device
    sys.stdout = open('nul', 'w')
    
    async def process_chunk(chunk, conversation, message_channel):
        response = conversation.run(chunk)
        chunked_response = [response[i:i + output_chunk_size] for i in range(0, len(response), output_chunk_size)]
        for cr in chunked_response:
            #Send a response to the channel where the original message was received
            print(" @", datetime.datetime.now().replace(microsecond=0))
            #Restore the standard output
            sys.stdout = original_stdout
            #This will not be printed to the console
            await message_channel.send(cr)

    async def process_chunks_concurrently(input_chunks, conversation, message_channel):
        await asyncio.gather(*[process_chunk(chunk, conversation, message.channel) for chunk in input_chunks])

    #Ignore message from the bot itself
    if message.author == bot.user:
        return
    
    if BOT_PREFIX_ON is True:
        if message.content.startswith(BOT_PREFIX):  # Check if the message starts with the prefix '/b'
            await process_chunks_concurrently(input_chunks, conversation, message.channel)
    else:
        await process_chunks_concurrently(input_chunks, conversation, message.channel)
        sys.stdout = original_stdout

#Run the bot with the specified API token
async def run_bot_async():
    await bot.start(API_TOKEN)

#Start the bot in a separate thread to avoid discord heartbeat blocking errors
asyncio.run(run_bot_async())