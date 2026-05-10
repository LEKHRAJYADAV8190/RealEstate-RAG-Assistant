# Generated from: rag.ipynb
# Converted at: 2026-05-10T12:43:30.061Z
# Next step (optional): refactor into modules & generate tests with RunCell
# Quick start: pip install runcell

from uuid import uuid4
from pathlib import Path
import os

from dotenv import load_dotenv

from langchain.chains import RetrievalQAWithSourcesChain
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_chroma import Chroma

from langchain_groq import ChatGroq

from langchain_huggingface.embeddings import HuggingFaceEmbeddings

from dotenv import load_dotenv
load_dotenv("env.txt")

import os
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv

from langchain_groq import ChatGroq

from langchain_community.document_loaders import WebBaseLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_chroma import Chroma

from langchain.chains import RetrievalQAWithSourcesChain

from langchain.prompts import PromptTemplate

from langchain.retrievers import ContextualCompressionRetriever

from langchain.retrievers.document_compressors import LLMChainExtractor


# =========================================================
# LOAD ENV
# =========================================================

load_dotenv()


# =========================================================
# CONFIG
# =========================================================

# BEST SMALL EMBEDDING MODEL
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

# CHUNKING
CHUNK_SIZE = 350
CHUNK_OVERLAP = 80

# VECTOR STORE
VECTORSTORE_DIR = Path.cwd() / "resources2/vectorstore2"

COLLECTION_NAME = "real_estate"

# GLOBALS
llm = None
vector_store = None


# =========================================================
# INITIALIZE COMPONENTS
# =========================================================

def initialize_components():

    global llm, vector_store

    print("\nInitializing Components...\n")

    # =====================================================
    # LLM
    # =====================================================

    if llm is None:

        print("Loading LLM...")

        llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),

            # BEST GROQ MODEL FOR RAG
            model_name="llama-3.3-70b-versatile",

            temperature=0,

            max_tokens=400
        )

        print("LLM Loaded ✅\n")

    # =====================================================
    # EMBEDDINGS
    # =====================================================

    if vector_store is None:

        print("Loading Embedding Model...")

        embedding_function = HuggingFaceEmbeddings(

            model_name=EMBEDDING_MODEL,

            model_kwargs={
                "device": "cpu"
            },

            encode_kwargs={
                "normalize_embeddings": True
            }
        )

        print("Embedding Model Loaded ✅\n")

        # =================================================
        # VECTOR STORE
        # =================================================

        print("Creating Chroma Vector Store...")

        vector_store = Chroma(
            collection_name=COLLECTION_NAME,

            embedding_function=embedding_function,

            persist_directory=str(VECTORSTORE_DIR)
        )

        print("Vector Store Ready ✅\n")


# =========================================================
# LOAD + PROCESS URLS
# =========================================================

def process_urls(urls):

    global vector_store

    initialize_components()

    print("\nLoading Articles...\n")

    # =====================================================
    # LOAD DATA
    # =====================================================

    loader = WebBaseLoader(
        web_paths=urls
    )

    data = loader.load()

    print(f"Loaded {len(data)} document(s) ✅\n")

    # =====================================================
    # CLEAN DATA
    # =====================================================

    cleaned_docs = []

    seen = set()

    for doc in data:

        text = doc.page_content.strip()

        # REMOVE DUPLICATES
        if text not in seen and len(text) > 200:

            seen.add(text)

            cleaned_docs.append(doc)

    print(f"Cleaned Docs: {len(cleaned_docs)} ✅\n")

    # =====================================================
    # SPLITTER
    # =====================================================

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=CHUNK_SIZE,

        chunk_overlap=CHUNK_OVERLAP,

        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    docs = splitter.split_documents(cleaned_docs)

    print(f"Created {len(docs)} chunks ✅\n")

    # =====================================================
    # STORE
    # =====================================================

    ids = [str(uuid4()) for _ in docs]

    vector_store.add_documents(
        documents=docs,
        ids=ids
    )

    print("Documents Stored in Chroma ✅\n")


# =========================================================
# CREATE RETRIEVER
# =========================================================

def create_retriever():

    global vector_store, llm

    # =====================================================
    # BASE RETRIEVER
    # =====================================================

    base_retriever = vector_store.as_retriever(

        search_type="mmr",

        search_kwargs={

            # FETCH MORE
            "fetch_k": 20,

            # FINAL RESULTS
            "k": 5,

            # DIVERSITY
            "lambda_mult": 0.7
        }
    )

    # =====================================================
    # CONTEXT COMPRESSION
    # =====================================================

    compressor = LLMChainExtractor.from_llm(llm)

    compression_retriever = ContextualCompressionRetriever(

        base_compressor=compressor,

        base_retriever=base_retriever
    )

    return compression_retriever


# =========================================================
# PROMPT
# =========================================================

QA_PROMPT = PromptTemplate(

    input_variables=["summaries", "question"],

    template="""
You are an intelligent RAG assistant.

Use ONLY the provided context to answer.

If answer is not present in context,
say:
"I could not find the answer in the article."

Give concise factual answers.

Always include:
- exact values
- dates
- percentages
- names

CONTEXT:
{summaries}

QUESTION:
{question}

ANSWER:
"""
)


# =========================================================
# GENERATE ANSWER
# =========================================================

def generate_answer(query):

    global llm

    print("\nGenerating Answer...\n")

    retriever = create_retriever()

    # =====================================================
    # QA CHAIN
    # =====================================================

    chain = RetrievalQAWithSourcesChain.from_chain_type(

        llm=llm,

        chain_type="stuff",

        retriever=retriever,

        return_source_documents=True,

        chain_type_kwargs={
            "prompt": QA_PROMPT
        }
    )

    # =====================================================
    # QUERY
    # =====================================================

    result = chain.invoke({
        "question": query
    })

    answer = result["answer"]

    sources = []

    for doc in result["source_documents"]:

        source = doc.metadata.get("source", "")

        if source and source not in sources:
            sources.append(source)

    return answer, sources


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    urls = [

        "https://www.cnbc.com/2024/12/20/why-mortgage-rates-jumped-despite-fed-interest-rate-cut.html",
        "https://www.cnbc.com/2024/12/21/how-the-federal-reserves-rate-policy-affects-mortgages.html"
    ]

    print("\n🚀 STARTING ADVANCED RAG PIPELINE\n")

    process_urls(urls)

    query = """
    What was the 30-year fixed mortgage rate mentioned in the article?
    Also provide the exact date.
    """

    answer, sources = generate_answer(query)

    # =====================================================
    # OUTPUT
    # =====================================================

    print("\n========================")
    print("ANSWER")
    print("========================\n")

    print(answer)

    print("\n========================")
    print("SOURCES")
    print("========================\n")

    for src in sources:
        print(src)