---
title: Echoes of History - Historical Persona Museum
emoji: 🏛️
colorFrom: brown
colorTo: amber
sdk: streamlit
sdk_version: 1.35.0
app_file: app.py
pinned: false
---

# 🏛️ The Historical Persona Museum (Echoes of History)

Step into the past and chat with historical personas! This is a Retrieval-Augmented Generation (RAG) chatbot application where you can interact with key historical figures like:
- **Abraham Lincoln** 🎩
- **Nikola Tesla** ⚡
- **Mahatma Gandhi** 🕊️
- **Donald Trump** 🦅
- **Grandfather** 👴

## Features
- **Retrieval-Augmented Generation (RAG)**: Powered by FAISS vectors storing authentic historical documents and letters.
- **Strict Boundaries**: Personas strictly adhere to their historical context and are unaware of events beyond their knowledge cutoff year.
- **Aesthetic Vintage UI**: Beautiful vintage parchment theme with micro-animations.
- **Interactive Lab**: Discover and register new personas dynamically by adding their source writings to `source_data/`.

## Running on Streamlit Community Cloud
This app is optimized for Streamlit Community Cloud. 

### How to Add your Groq API Key
To make sure the app can run securely without exposing your credentials:
1. Go to your [Streamlit Share Dashboard](https://share.streamlit.io/).
2. Locate your deployed app, click the three dots (`...`) on the right, and select **Settings**.
3. In the settings menu, click on the **Secrets** tab.
4. Paste your Groq API Key in TOML format:
   ```toml
   GROQ_API_KEY = "your_groq_api_key_here"
   ```
5. Click **Save**. Streamlit will automatically restart the app with the credentials injected!

