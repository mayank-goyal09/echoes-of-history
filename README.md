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
This app is optimized for Hugging Face Spaces and runs using the free serverless Hugging Face Inference API.
- **Model**: `Qwen/Qwen2.5-7B-Instruct` (or any custom open-source instruction model).
- **Authentication**: On Hugging Face Spaces, it automatically uses the `HF_TOKEN` environment variable injected by the Space.
