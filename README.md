# FounderMentor AI Agent

This repository contains an AI-powered agent designed to answer questions based on *The Strategy Files* newsletter content. The agent uses [Chroma](https://www.trychroma.com/) as a vector database to store and search newsletter embeddings, combined with OpenAI's GPT models to generate intelligent, context-aware answers.

## Features

- Ingests newsletter content and converts it into vector embeddings for efficient semantic search.
- Answers user queries by retrieving relevant newsletter sections and generating responses with GPT.
- Designed to support the [FounderMentor](https://github.com/your-username/foundermentor) ecosystem as a microservice or standalone AI assistant.
- Easily extendable to other content sources or integrated into Rails/React apps.

## Getting Started

1. Create a Python virtual environment:
   ```bash
   python3 -m venv chroma-env
   source chroma-env/bin/activate
2. Install the dependencies
   pip install -r requirements.txt
3. Add your OpenAI API key to environment variables or config, e.g.:
  export OPENAI_API_KEY="your_api_key_here"
4. Run the example script
   python chroma_test.py
   ```
## What does chroma_test.py do?
Sets up Chroma with local persistence

Adds sample newsletter snippets as vectors

Queries by semantic similarity

Passes the best matching snippet + user question to GPT

Prints the answer

## How to run it
source chroma-env/bin/activate

## What does requirements.txt do?
chromadb — The vector database library for embeddings and search
openai — Official OpenAI Python SDK to call GPT and embedding APIs
python-dotenv — For managing environment variables easily (optional but recommended)


## License

MIT License
