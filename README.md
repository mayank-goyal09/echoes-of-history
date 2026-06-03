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

## Running on Hugging Face Spaces
This app is fully compatible with Hugging Face Spaces and runs using the Streamlit SDK.

### Configuration
Since the app uses Groq for fast inference, you need to add your Groq API Key as a repository secret:
1. Go to your **Space Settings** on Hugging Face.
2. Scroll down to **Variables and Secrets** and click **New Secret**.
3. Name the secret `GROQ_API_KEY` and paste your Groq API key (e.g. `gsk_...`) as the value.
4. Save the secret and restart your Space if it is already running. The app will automatically read it and start functioning!
