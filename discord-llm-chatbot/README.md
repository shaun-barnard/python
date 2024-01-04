## Python Discord LLM Chatbot

Basic Discord chatbot using [Discord.py](https://github.com/Rapptz/discord.py) and [LangChain](https://github.com/langchain-ai/langchain). The bot is designed to interact with Discord channel users in a conversational manner, leveraging language models (LLM), and conversational memory to provide engaging responses.

## Installation

### 1. Initialize a new Git repository on your local machine
```bash
git init <repo>
cd <repo>
```

### 2. Add this repository to the specific folder:
```bash
git remote add -f origin https://github.com/shaunbarnard/python.git
```

### 3. Enable the sparse-checkout feature and specify the folder you want to clone. In this case (llm-discord-chatbot):
```bash
git sparse-checkout init --cone
git sparse-checkout set llm-discord-chatbot
```

### 4. Finally, check out the contents of the specified folder (llm-discord-chatbot)
```bash
git checkout @
```