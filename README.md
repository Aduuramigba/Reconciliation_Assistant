# Reconciliation Assistant

**AI-powered voice-enabled knowledge assistant for enterprise reconciliation workflows**

This project is a Retrieval-Augmented Generation (RAG) assistant built to help teams query reconciliation knowledge more efficiently. It combines document ingestion, vector search, conversational memory, and a voice agent interface so users can ask questions about reconciliation processes and receive grounded answers from an internal knowledge base.

## Why this project matters

In enterprise operations, reconciliation teams often depend on product documents, implementation guides, and support knowledge that are slow to search manually. This project shows how an AI assistant can improve that workflow by:

- turning internal documentation into a searchable knowledge base
- answering questions using retrieval instead of pure model memory
- supporting voice-based interaction for faster access
- keeping responses grounded in the provided knowledge source

## What I built

The assistant has two core layers:

### 1) Knowledge ingestion pipeline
I built a document ingestion flow that:

- loads markdown files from a local `data/` directory
- splits documents into chunks for retrieval
- extracts image paths from markdown content into metadata
- generates embeddings with OpenAI
- stores the embeddings in a persistent Chroma vector database

### 2) Voice-enabled conversational agent
I built a voice agent that:

- uses **speech-to-text** to capture user queries
- uses a **retrieval chain** to fetch relevant document context
- generates answers with an LLM
- uses **text-to-speech** to reply back to the user
- tracks runtime metrics for LLM, STT, TTS, and end-of-utterance events

This makes the project more than a simple chatbot. It is closer to a real AI support assistant designed for enterprise use.

## Technical highlights

- **RAG architecture** using LangChain + Chroma
- **Persistent vector store** for reusable document search
- **Conversational memory** for context-aware follow-up questions
- **Voice interface** using LiveKit + OpenAI STT/TTS
- **Prompt-constrained responses** to reduce hallucinations
- **Metrics instrumentation** for monitoring response behavior
- **Modular code structure** separating ingestion, retrieval, prompt instructions, and agent runtime

## Architecture overview

```text
User (voice/text)
   ↓
Speech-to-Text / Query Input
   ↓
LiveKit Agent
   ↓
LangChain Conversational Retrieval Chain
   ↓
Chroma Vector Store
   ↓
Embedded Knowledge Base from internal documents
   ↓
LLM Response Generation
   ↓
Text-to-Speech output
```

## Project structure

```text
Reconciliation_Assistant/
├── data/               # knowledge documents used for ingestion
├── chroma_db/          # persisted vector store
├── ingest.py           # builds embeddings and stores chunks in Chroma
├── my_tool.py          # retrieval chain and conversational memory
├── prompt.py           # system instructions and welcome message
├── my_agent.py         # voice agent runtime with LiveKit + OpenAI
├── requirements.txt    # project dependencies
└── .env                # environment variables
```

## Tools and technologies

- **Python**
- **LangChain**
- **Chroma Vector DB**
- **OpenAI Embeddings**
- **OpenAI GPT models**
- **Whisper STT**
- **OpenAI TTS**
- **LiveKit Agents**
- **python-dotenv**

## How it works

### Step 1: Ingest documents
The ingestion script loads markdown documents from the `data/` folder, splits them into chunks, attaches image metadata, embeds the chunks, and persists them into Chroma.

### Step 2: Create the retrieval chain
The retrieval layer loads the Chroma database, initializes an OpenAI chat model, attaches conversation memory, and exposes a conversational retrieval chain.

### Step 3: Run the voice agent
The agent accepts spoken input, transcribes it, calls the retrieval tool to search the knowledge base, generates a grounded answer, and responds with synthesized speech.

## Example use cases

- Internal support assistant for reconciliation platforms
- Knowledge assistant for operations teams
- Voice-based document QA for enterprise software
- Faster onboarding tool for support and implementation staff

## What this project demonstrates to recruiters

This repository reflects hands-on ability to:

- design and build a practical **RAG application**
- integrate **LLMs with enterprise knowledge workflows**
- connect **voice AI pipelines** to business use cases
- structure an AI application into reusable components
- work across **retrieval, prompting, embeddings, vector search, and agent orchestration**

It also shows awareness of a real business problem: helping support or operations teams get trustworthy answers from internal documentation faster.

## Key engineering decisions

- I used **retrieval-based answering** so the system responds from the knowledge base instead of relying only on base model memory.
- I used a **persistent vector database** so ingestion only needs to happen once unless documents change.
- I added **conversation memory** so follow-up questions feel natural.
- I used a **voice interface** to make the assistant usable beyond a standard text chatbot.
- I constrained the prompt to encourage grounded responses and avoid unsupported claims.

## Setup

### 1) Clone the repository
```bash
git clone <your-repo-url>
cd Reconciliation_Assistant
```

### 2) Create a virtual environment
```bash
python -m venv venv
```

Activate it:

**Windows**
```bash
venv\Scripts\activate
```

**macOS/Linux**
```bash
source venv/bin/activate
```

### 3) Install dependencies
```bash
pip install -r requirements.txt
```

### 4) Add environment variables
Create a `.env` file and add the required keys, for example:

```env
OPENAI_API_KEY=your_key_here
```

You may also need any LiveKit-related environment settings depending on how you run the voice agent.

## Run the project

### Build the knowledge base
```bash
python ingest.py
```

### Start the assistant
```bash
python my_agent.py
```

## Future improvements

Planned or possible next steps:

- add a web UI for text + voice interaction
- support PDF ingestion directly
- improve observability with structured logging and dashboards
- add citations/snippets from retrieved sources in responses
- replace buffer memory with a more scalable memory strategy
- containerize deployment for production usage

## Recruiter-friendly summary

**Reconciliation Assistant** is an enterprise-focused AI project that applies RAG, vector search, and voice AI to a real support workflow. It demonstrates practical experience building LLM-powered systems that are grounded in business knowledge, modular in design, and relevant to enterprise operations.


---

## Author

**Omosule Aduramigba Adeleke**  
AI Engineer | Backend Developer | Enterprise Support / Reconciliation Domain Experience

If you're hiring for AI engineering, backend AI integration, or LLM application development, this project reflects practical work on real-world enterprise use cases.
