<p align="center">
  <a href="#installation" style="font-size: 24px;">Install</a> |
  <a href="#download-llm-large-language-model" style="font-size: 24px;">Download LLM</a> |
  <a href="#create-a-discord-application" style="font-size: 24px;">Create Discord Application</a> |
  <a href="#configuration" style="font-size: 24px;">Configuration</a> |
  <a href="#run-the-bot" style="font-size: 24px;">Run</a>
</p>

## Python Discord LLM (Large Language Model) Chatbot

A basic Discord chatbot using [Discord.py](https://github.com/Rapptz/discord.py), [LangChain](https://github.com/langchain-ai/langchain), and [GPT4ALL](https://github.com/nomic-ai/gpt4all). The bot is designed to interact with Discord channel users in a conversational manner, leveraging large language models (LLM), and conversational memory to provide engaging responses.

## Installation

> [!IMPORTANT]
> Requires atleast Python 3.10 to work.

#### 1. Create and activate a virtual enviroment
```bash
conda update conda
conda create -n <env name> python=3.10
conda activate <env name>
```

#### 2. Create a new folder for this repository
```bash
mkdir <repo>
cd <repo>
```

#### 3. Create a treeless, shallow clone of this repository
```bash
git clone -n --depth=1 --filter=tree:0 https://github.com/shaunbarnard/python.git
cd python
```

#### 4. Enable the sparse-checkout feature and specify the folder you want to clone (discord-llm-chatbot)
```bash
git sparse-checkout set --no-cone discord-llm-chatbot
```

#### 5. Check out the contents of the specified folder (llm-discord-chatbot)
```bash
git checkout
cd discord-llm-chatbot
```

#### 6. Install the necessary Python dependencies
```bash
pip install -r requirements.txt
``` 

## Download LLM (Large Language Model)
Skip if you've already have a model, otherwise head over to [HuggingFace.co](https://huggingface.co/models?pipeline_tag=text-generation&sort=trending&search=.GGUF) and download a model.

#### If you have shitty internet, you're gonna want to create a custom download script to avoid wanting to punch a hole through your monitor...

#### 1. Create a new file
```bash
sudo nano red.sh
```

#### 2. Copy and paste the following into the newly created file:
```bash
#!/bin/bash

while true
do
    wget -c --retry-connrefused --waitretry=1 --read-timeout=20 --timeout=15 -t 0 "https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF/resolve/main/mistral-7b-v0.1.Q4_K_M.gguf?download=true"
    sleep 10s
done
```

*Note: If you need to replace the URL, make sure to include the '?download=true' parameter.*

#### 3. Set the download script file permissions to executable
```bash
sudo chmod 775 red.sh
```

#### 4. Run the download script
```bash
./red.sh
```

*Note: The download script will contiunally retry and resume failed downloads, even if connection cuts out. Once download is complete, you'll need to manually kill the script.*

#### 5. Rename the downloaded file
```bash
sudo mv 'mistral-7b-v0.1.Q4_K_M.gguf?download=true' mistral-7b-v0.1.Q4_K_M.gguf
```

## Create a Discord Application:

### Create a Discord Bot
1. Log in to the [Discord Developer Portal](https://discord.com/login?redirect_to=%2Fdevelopers%2Fapplications)
2. Click on the "New Application" button
3. Give your application a name and confirm the creation

### Create a Bot Account
1. Navigate to the "Bot" tab to configure the bot
2. Check the "Public Bot" option if you want others to invite your bot
3. Tick the "bot" checkbox under "scopes" and set the necessary permissions for your bot
4. Copy the bot's token to use it in your bot's code

### Add the Bot to a Discord Server
1. Use the bot's token to invite the bot to your Discord server
2. Set the appropriate permissions for your bot

*Note: Above steps are a general overview of the process. For detailed instructions and best practices, you can refer to the [Offical Discord Documentation](https://discord.com/developers/docs/intro)*

## Configuration

**1. Set the model path in [bot.py](https://github.com/shaunbarnard/python/blob/main/discord-llm-chatbot/bot.py?plain=1#L17) to your model's location.**

```py
#Set model path
model_path = ("mistral-7b-v0.1.Q4_K_M.gguf")
```

**2. Adjust the remaining configuration settings in [bot.py](https://github.com/shaunbarnard/python/blob/main/discord-llm-chatbot/bot.py?plain=#L18-L21) as necessary**

```py
BOT_PREFIX_ON = True
BOT_PREFIX = '/b'
BOT_CHANNEL_MESSAGE_ON = True
BOT_CHANNEL_MESSAGE = "Hey guys! Use '/b' followed by your message to interact with me ;)"
```

**3. Create an .env file to your store Discord Bot's API Token**

```bash
sudo nano .env
```

**4. Paste your API Token into the newly created .env file**

```bash
API_KEY=<your bot's discord token>
```

## Run the bot

```bash
python bot.py
```