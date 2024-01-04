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

### 3. Enable the sparse-checkout feature and specify the folder you want to clone. In our case (discord-llm-chatbot):
```bash
git sparse-checkout set --no-cone discord-llm-chatbot
```

### 4. Finally, check out the contents of the specified folder (llm-discord-chatbot)
```bash
git checkout
cd discord-llm-chatbot
```

## Download LLM Model
Skip this if you already have a model, otherwise head over to [HuggingFace.co](https://huggingface.co/models?pipeline_tag=text-generation&sort=trending&search=.GGUF) and download a model.

#### If you have shitty internet, you're gonna want to create a custom download script to avoid wanting to punch a hole through your monitor...
```bash
nano red.sh
```

#### Copy and paste the script below. 

```bash
#!/bin/bash

while true
do
    wget -c --retry-connrefused --waitretry=1 --read-timeout=20 --timeout=15 -t 0 "https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF/resolve/main/mistral-7b-v0.1.Q4_K_M.gguf?download=true"
    sleep 10s
done
```

Note: If you need to replace the URL, make sure to include the '?download=true' parameter.

#### Set permissions
```bash
sudo chmod 775 red,sh
```

#### Run script
```bash
./red.sh
```

The download script will contiunally retry and resume failed downloads even if connection cuts out. Once it finishes downloading, you'll need to manually kill the script otherwise it'll flood your cli bitching about the download being complete.