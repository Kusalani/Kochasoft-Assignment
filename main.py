"""
Graph RAG Implementation using Groq API
This solves the timeout issues by using Groq's fast inference
"""

import os
import nest_asyncio
from llama_index.core import KnowledgeGraphIndex, SimpleDirectoryReader, Settings, StorageContext
from llama_index.graph_stores.neo4j import Neo4jGraphStore
from llama_index.llms.groq import Groq
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.node_parser import SimpleNodeParser
from config import config
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

nest_asyncio.apply()

# Groq API configuration
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "#####")

def setup_groq_llm():
    """Setup Groq LLM with fast inference"""
    
    
    llm = Groq(
        model="llama3-8b-8192",  # Good balance of speed and capability
        api_key=GROQ_API_KEY,
        temperature=0.1,  # Low temperature for consistent extraction
        max_tokens=2048,
    )
    
    return llm

def create_graph_index_with_groq():
    """Create knowledge graph using Groq for fast processing"""
    
    # Setup Groq LLM
    llm = setup_groq_llm()
    Settings.llm = llm
    
    # Keep Ollama for embeddings (or use HuggingFace)
    embed_model = OllamaEmbedding(
        model_name=config.OLLAMA_EMBED_MODEL,
        base_url=f"http://{config.OLLAMA_HOST}:{config.OLLAMA_PORT}",
        request_timeout=300.0
    )
    Settings.embed_model = embed_model
    
    # Load documents
    loader = SimpleDirectoryReader(
        input_dir=config.DOC_DIR,
        required_exts=[".pdf"],
        recursive=True
    )
    docs = loader.load_data()
    logger.info(f"Loaded {len(docs)} documents")
    
    # Create nodes with reasonable chunk size
    node_parser = SimpleNodeParser.from_defaults(
        chunk_size=1024,  # Can use larger chunks with Groq
        chunk_overlap=100
    )
    nodes = node_parser.get_nodes_from_documents(docs)
    logger.info(f"Created {len(nodes)} nodes")
    
    # Setup Neo4j
    graph_store = Neo4jGraphStore(
        username=config.NEO4J_USERNAME,
        password=config.NEO4J_PASSWORD,
        url=config.NEO4J_URI,
        database="neo4j",
        timeout=30.0
    )
    storage_context = StorageContext.from_defaults(graph_store=graph_store)
    
    # Create knowledge graph with Groq's fast inference
    logger.info("Building knowledge graph with Groq...")
    
    try:
        kg_index = KnowledgeGraphIndex(
            nodes=nodes,
            storage_context=storage_context,
            max_triplets_per_chunk=5,  # Can handle more with Groq's speed
            include_embeddings=True,
            show_progress=True
        )
        
        logger.info("Knowledge graph created successfully!")
        
        # Save index
        kg_index.storage_context.persist(persist_dir="./storage_groq")
        logger.info("Index saved to ./storage_groq")
        
        return kg_index
        
    except Exception as e:
        logger.error(f"Error creating graph: {e}")
        raise

def main():
    """Main function with Groq implementation"""
    
    print("\n" + "="*60)
    print("Graph RAG with Groq API - Fast Inference Solution")
    print("="*60)
    
    # Check API key
    if GROQ_API_KEY == "your-groq-api-key-here":
        print("\n⚠️  Please set your GROQ_API_KEY environment variable!")
        print("Get your free API key at: https://console.groq.com/keys")
        print("\nExample: export GROQ_API_KEY='your-key-here'")
        return
    
    # Create or load index
    if os.path.exists("./storage_groq"):
        logger.info("Loading existing index...")
        from llama_index.core import load_index_from_storage
        storage_context = StorageContext.from_defaults(persist_dir="./storage_groq")
        kg_index = load_index_from_storage(storage_context)
    else:
        kg_index = create_graph_index_with_groq()
    
    # Create query engine
    from llama_index.core.query_engine import RetrieverQueryEngine
    from llama_index.core.retrievers import KnowledgeGraphRAGRetriever
    
    graph_rag_retriever = KnowledgeGraphRAGRetriever(
        storage_context=kg_index.storage_context,
        verbose=True,
    )
    
    query_engine = RetrieverQueryEngine.from_args(
        graph_rag_retriever,
    )
    
    # Interactive query loop
    print("\n✅ System ready! Groq's fast inference eliminates timeout issues.")
    print("Enter your questions below:\n")
    
    while True:
        user_query = input("\nQuestion (or 'quit' to exit): ")
        if user_query.lower() in ['quit', 'exit', 'q']:
            break
            
        try:
            print("\nProcessing with Groq...")
            response = query_engine.query(user_query)
            print(f"\nAnswer: {response}")
        except Exception as e:
            logger.error(f"Query error: {e}")
            print("Error processing query. Please try again.")

if __name__ == "__main__":
    main()