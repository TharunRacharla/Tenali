import os
from llama_index.llms.ollama import OLLama
from llama_index.core import (
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
    Settings
)

# Persist directory for the index (can be overridden with env var)
PERSIST_DIR = os.getenv("PERSIST_DIR", "PERSIST_DIR")

from llama_index.embeddings.huggingface import HuggingFaceEmbedding

#Setup llm and embedding models
embed_model = HuggingFaceEmbedding(model_name="BAAI-bge-small-en-v1.5")
llm = OLLama(model="gemma3", request_timeout=120.0)
Settings.llm = llm
Settings.embed_model = embed_model

# check if our index already exists
if not os.path.exists(PERSIST_DIR):
    documents = SimpleDirectoryReader('tenali/ml_models/data').load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)