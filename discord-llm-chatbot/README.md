## Python Discord LLM Chatbot

Basic Discord chatbot using [Discord.py](https://github.com/Rapptz/discord.py) and [LangChain](https://github.com/langchain-ai/langchain). The bot is designed to interact with Discord channel users in a conversational manner, leveraging language models (LLM), and conversational memory to provide engaging responses.

## Installation

### 1. Create new folder for repo on your local machine
```bash
mkdir <repo>
cd <repo>
```

### 2. Create a treeless, shallow clone of the repo
```bash
git clone -n --depth=1 --filter=tree:0 https://github.com/shaunbarnard/python.git
cd python
```

### 3. Enable the sparse-checkout feature and specify the folder you want to clone. In this case (llm-discord-chatbot):
```bash
git sparse-checkout set --no-cone discord-llm-chatbot
```

### 4. Finally, check out the contents of the specified folder (llm-discord-chatbot)
```bash
git checkout
cd discord-llm-chatbot
```