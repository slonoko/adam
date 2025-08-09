import logging
import os
import sys
import vertexai
from vertexai import rag
from typing import Dict, Optional, Any
from dotenv import load_dotenv
from fastmcp import FastMCP, Client
from google.oauth2 import service_account
import json

load_dotenv()

# RAG Corpus Settings
RAG_DEFAULT_TOP_K = 10  # Default number of results for single corpus query
RAG_DEFAULT_SEARCH_TOP_K = 5  # Default number of results per corpus for search_all
RAG_DEFAULT_VECTOR_DISTANCE_THRESHOLD = 0.5

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Create an MCP server
mcp = FastMCP("corpora_search")

def load_credentials_from_file(service_account_path: str):
    """Loads Google Cloud credentials from a service account JSON file."""
    try:
        return service_account.Credentials.from_service_account_file(service_account_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Service account file not found: {service_account_path}")
    except Exception as e:
        raise RuntimeError(f"Error loading credentials from {service_account_path}: {e}")

def get_project_id_from_file(service_account_path: str) -> str:
    """Extracts the project_id from the service account JSON file."""
    try:
        with open(service_account_path, 'r') as f:
            data = json.load(f)
            project_id = data.get("project_id")
            if not project_id:
                raise ValueError("Key 'project_id' not found in service account file.")
            return project_id
    except FileNotFoundError:
        raise FileNotFoundError(f"Service account file not found: {service_account_path}")
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        raise RuntimeError(f"Error reading project_id from {service_account_path}: {e}")

SERVICE_ACCOUNT_FILE = "adam-sa.json"
PROJECT_NAME = get_project_id_from_file(SERVICE_ACCOUNT_FILE)
PROJECT_LOCATION = "us-central1"
creds = load_credentials_from_file(SERVICE_ACCOUNT_FILE)

# Initialize Vertex AI API
vertexai.init(credentials=creds, project=PROJECT_NAME, location=PROJECT_LOCATION)

@mcp.tool
def list_rag_corpora() -> Dict[str, Any]:
    """
    Lists all RAG corpora in the current project and location.
    
    Returns:
        A dictionary containing the list of corpora:
        - status: "success" or "error"
        - corpora: List of corpus objects with id, name, and display_name
        - count: Number of corpora found
        - error_message: Present only if an error occurred
    """
    return __list_rag_corpora()

def __list_rag_corpora() -> Dict[str, Any]:
    try:
        corpora = rag.list_corpora()
        
        corpus_list = []
        for corpus in corpora:
            logging.info(f"Found RAG corpus: {corpus.name}")    
            corpus_id = corpus.name.split('/')[-1]
            
            # Get corpus status
            status = None
            if hasattr(corpus, "corpus_status") and hasattr(corpus.corpus_status, "state"):
                status = corpus.corpus_status.state
            elif hasattr(corpus, "corpusStatus") and hasattr(corpus.corpusStatus, "state"):
                status = corpus.corpusStatus.state
            
            # Make an explicit API call to count files
            files_count = 0
            try:
                # List all files to get the count
                files_response = rag.list_files(corpus_name=corpus.name)
                
                if hasattr(files_response, "rag_files"):
                    files_count = len(files_response.rag_files)
            except Exception:
                # If counting files fails, continue with zero count
                pass
            
            corpus_list.append({
                "id": corpus_id,
                "name": corpus.name,
                "display_name": corpus.display_name,
                "description": corpus.description if hasattr(corpus, "description") else None,
                "create_time": str(corpus.create_time) if hasattr(corpus, "create_time") else None,
                "files_count": files_count,
                "status": status
            })
        
        return {
            "status": "success",
            "corpora": corpus_list,
            "count": len(corpus_list),
            "message": f"Found {len(corpus_list)} RAG corpora"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e),
            "message": f"Failed to list RAG corpora: {str(e)}"
        }

@mcp.tool
def query_rag_corpus(
    corpus_path: str,
    query_text: str,
    top_k: Optional[int] = None,
    vector_distance_threshold: Optional[float] = None
) -> Dict[str, Any]:
    """
    Directly queries a RAG corpus using the Vertex AI RAG API.
    
    Args:
        corpus_id: The ID of the corpus to query
        query_text: The search query text
        top_k: Maximum number of results to return (default: 10)
        vector_distance_threshold: Threshold for vector similarity (default: 0.5)
        
    Returns:
        A dictionary containing the query results
    """

    return __query_rag_corpus(
        corpus_path=corpus_path,
        query_text=query_text,
        top_k=top_k,
        vector_distance_threshold=vector_distance_threshold
    )

def __query_rag_corpus(
    corpus_path: str,
    query_text: str,
    top_k: Optional[int] = None,
    vector_distance_threshold: Optional[float] = None
) -> Dict[str, Any]:
    if top_k is None:
        top_k = RAG_DEFAULT_TOP_K
    if vector_distance_threshold is None:
        vector_distance_threshold = RAG_DEFAULT_VECTOR_DISTANCE_THRESHOLD
    try:
        
        # Create the resource config
        rag_resource = rag.RagResource(rag_corpus=corpus_path)
        
        # Configure retrieval parameters
        retrieval_config = rag.RagRetrievalConfig(
            top_k=top_k,
            filter=rag.Filter(
                vector_distance_threshold=vector_distance_threshold)
        )
        
        # Execute the query directly using the API
        response = rag.retrieval_query(
            rag_resources=[rag_resource],
            text=query_text,
            rag_retrieval_config=retrieval_config
        )
        
        # Process the results
        results = []
        if hasattr(response, "contexts"):
            # Handle different response structures
            contexts = response.contexts
            if hasattr(contexts, "contexts"):
                contexts = contexts.contexts
            
            # Extract text and metadata from each context
            for context in contexts:
                result = {
                    "text": context.text if hasattr(context, "text") else "",
                    "source_uri": context.source_uri if hasattr(context, "source_uri") else None,
                    "relevance_score": context.relevance_score if hasattr(context, "relevance_score") else None
                }
                results.append(result)
        
        return {
            "status": "success",
            "corpus_path": corpus_path,
            "results": results,
            "count": len(results),
            "query": query_text,
            "message": f"Found {len(results)} results for query: '{query_text}'"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "corpus_path": corpus_path,
            "error_message": str(e),
            "message": f"Failed to query corpus: {str(e)}"
        }

@mcp.tool
def search_all_corpora(
    query_text: str,
    top_k_per_corpus: Optional[int] = None,
    vector_distance_threshold: Optional[float] = None
) -> Dict[str, Any]:
    """
    Searches across ALL available corpora for the given query text.
    When a user wants to search for information without specifying a corpus,
    this is the default tool to use.
    
    Args:
        query_text: The search query text
        top_k_per_corpus: Maximum number of results to return per corpus (default: 5)
        vector_distance_threshold: Threshold for vector similarity (default: 0.5)
        
    Returns:
        A dictionary containing the combined search results with citations
    """
    if top_k_per_corpus is None:
        top_k_per_corpus = RAG_DEFAULT_SEARCH_TOP_K
    if vector_distance_threshold is None:
        vector_distance_threshold = RAG_DEFAULT_VECTOR_DISTANCE_THRESHOLD
    try:
        # First, list all available corpora
        corpora_response = __list_rag_corpora()
        
        if corpora_response["status"] != "success":
            return {
                "status": "error",
                "error_message": f"Failed to list corpora: {corpora_response.get('error_message', '')}",
                "message": "Failed to search all corpora - could not retrieve corpus list"
            }
        
        all_corpora = corpora_response.get("corpora", [])
        
        if not all_corpora:
            return {
                "status": "warning",
                "message": "No corpora found to search in"
            }
        
        # Search in each corpus
        all_results = []
        corpus_results_map = {}  # Map of corpus name to its results
        searched_corpora = []
        
        for corpus in all_corpora:
            corpus_path = corpus["name"]
            corpus_id = corpus["id"]
            corpus_name = corpus["display_name"] or corpus["name"]
            
            # Query this corpus
            corpus_results = __query_rag_corpus(
                corpus_path=corpus_path,
                query_text=query_text,
                top_k=top_k_per_corpus,
                vector_distance_threshold=vector_distance_threshold
            )
            
            # Add corpus info to the results
            if corpus_results["status"] == "success":
                results = corpus_results.get("results", [])
                corpus_specific_results = []
                
                for result in results:
                    # Add citation and source information
                    result["corpus_id"] = corpus_id
                    result["corpus_name"] = corpus_name
                    result["citation"] = f"[Source: {corpus_name} ({corpus_id})]"
                    
                    # Add source file information if available
                    if "source_uri" in result and result["source_uri"]:
                        source_path = result["source_uri"]
                        file_name = source_path.split("/")[-1] if "/" in source_path else source_path
                        result["citation"] += f" File: {file_name}"
                    
                    corpus_specific_results.append(result)
                    all_results.append(result)
                
                # Save results for this corpus
                if corpus_specific_results:
                    corpus_results_map[corpus_name] = {
                        "corpus_id": corpus_id,
                        "corpus_name": corpus_name,
                        "results": corpus_specific_results,
                        "count": len(corpus_specific_results)
                    }
                    searched_corpora.append(corpus_name)
        
        # Sort all results by relevance score (if available)
        all_results.sort(
            key=lambda x: x.get("relevance_score", 0) if x.get("relevance_score") is not None else 0,
            reverse=True
        )
        
        # Format citations summary
        citations_summary = []
        for corpus_name in searched_corpora:
            corpus_data = corpus_results_map[corpus_name]
            citations_summary.append(
                f"{corpus_name} ({corpus_data['corpus_id']}): {corpus_data['count']} results"
            )
        
        return {
            "status": "success",
            "results": all_results,
            "corpus_results": corpus_results_map,
            "searched_corpora": searched_corpora,
            "citations_summary": citations_summary,
            "count": len(all_results),
            "query": query_text,
            "message": f"Found {len(all_results)} results for query '{query_text}' across {len(searched_corpora)} corpora",
            "citation_note": "Each result includes a citation indicating its source corpus and file."
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e),
            "message": f"Failed to search all corpora: {str(e)}"
        }

""" client = Client(mcp)

async def call_tool(query: str):
    async with client:
        result = await client.call_tool("search_all_corpora", {"query_text": query})
        print(result)

asyncio.run(call_tool("stock options"))
 """
""" 
if __name__ == "__main__":
    mcp.run(transport="http",log_level="debug",port=8000) """