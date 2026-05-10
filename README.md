# 🏡 Real Estate Research Tool

> **AI-powered RAG pipeline** that lets you ask questions about any real estate article — just paste URLs, process them, and query away.

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-F55036?style=for-the-badge&logo=groq&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-6C3483?style=for-the-badge)
![HuggingFace](https://img.shields.io/badge/HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)

---

## ✨ What It Does

Paste real estate article URLs → the tool scrapes, chunks, embeds, and stores them in a local vector DB. Then ask any natural language question and get **precise, source-cited answers** powered by LLaMA 3.3 70B via Groq.

---

## 🖥️ Demo

```
📎 Paste URLs  →  🚀 Process  →  💬 Ask Questions  →  📌 Get Answers + Sources
```

---

## 🧠 Architecture

```
URLs
 │
 ▼
WebBaseLoader (LangChain)
 │  Scrapes raw HTML
 ▼
Text Cleaning & Deduplication
 │  Removes junk & duplicates
 ▼
RecursiveCharacterTextSplitter
 │  chunk_size=350 | overlap=80
 ▼
HuggingFace Embeddings
 │  BAAI/bge-small-en-v1.5
 ▼
ChromaDB Vector Store  ←──────────────────┐
 │  Persisted locally                     │
 ▼                                        │
MMR Retriever (fetch_k=20, k=5)           │
 │  Diversity-aware retrieval             │
 ▼                                        │
LLMChainExtractor (Contextual Compression)│
 │  Filters irrelevant context            │
 ▼                                        │
RetrievalQAWithSourcesChain               │
 │  Groq LLaMA-3.3-70b-versatile          │
 ▼                                        │
Answer + Source URLs ─────────────────────┘
```

---

## 🗂️ Project Structure

```
real-estate-rag/
│
├── main.py                  # Streamlit UI
├── rag.py                   # RAG pipeline (load, embed, retrieve, generate)
├── env.txt                  # API keys (not committed)
├── resources2/
│   └── vectorstore2/        # Persisted ChromaDB
└── README.md
```

---

## ⚙️ Tech Stack

| Component | Tool |
|-----------|------|
| **UI** | Streamlit |
| **LLM** | Groq — `llama-3.3-70b-versatile` |
| **Embeddings** | `BAAI/bge-small-en-v1.5` (HuggingFace) |
| **Vector DB** | ChromaDB (local persist) |
| **Retrieval** | MMR + Contextual Compression |
| **Framework** | LangChain |

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/real-estate-rag.git
cd real-estate-rag
```

### 2. Install dependencies

```bash
pip install streamlit langchain langchain-community langchain-groq \
            langchain-huggingface langchain-chroma chromadb \
            python-dotenv unstructured
```

### 3. Set up your API key

Create a file called `env.txt` in the root:

```
GROQ_API_KEY=your_groq_api_key_here
```

> 🔑 Get your free Groq API key at [console.groq.com](https://console.groq.com)

### 4. Run the app

```bash
streamlit run main.py
```

---

## 💡 How to Use

1. **Add URLs** — click ➕ in the sidebar and paste real estate article URLs
2. **Process** — hit 🚀 Process URLs to scrape, chunk & embed
3. **Ask** — type any question in the query box
4. **Get answers** — see the AI-generated answer + source links

---

## 🔧 Configuration (in `rag.py`)

| Parameter | Default | Description |
|-----------|---------|-------------|
| `EMBEDDING_MODEL` | `BAAI/bge-small-en-v1.5` | HuggingFace embedding model |
| `CHUNK_SIZE` | `350` | Characters per chunk |
| `CHUNK_OVERLAP` | `80` | Overlap between chunks |
| `fetch_k` | `20` | Candidates fetched by MMR |
| `k` | `5` | Final chunks passed to LLM |
| `lambda_mult` | `0.7` | MMR diversity factor (0=max diversity, 1=max relevance) |
| `max_tokens` | `400` | Max tokens in LLM response |

---

## 📦 Run Without UI (CLI)

```bash
python rag.py
```

This runs the pipeline directly on two sample CNBC articles and prints the answer to the terminal.

---

## 🙏 Credits

Built by **Dhaval Patel** — [Codebasics Inc.](https://codebasics.io) & LearnerX Pvt Ltd.

---

## 📄 License

© Codebasics Inc. and LearnerX Pvt Ltd. All rights reserved.
