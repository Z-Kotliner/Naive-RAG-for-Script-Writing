from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from .llm_service import LLMClient

# Create messages
messages = [
    ("human",
     """You are a helpful AI assistant that re-writes user user query to improve search precision. \n
      The context of the application is about searching movie scripts.
      The re-written query will be used to perform similarity search on a vector store that contains all scenes in the script. \n

      Make sure the query emphasis crucial keywords of the query for good scene retrieval.

      Respond only with the re-written query and nothing else. Do not put options with 'or'.

      Example:

      query - "Only scenes involving trains"
      output - "Find scenes featuring trains"


     """
     ),
    ("user", "{query}")
]


def rewrite_query(query) -> str:
    # Create a prompt
    prompt = ChatPromptTemplate.from_messages(messages)

    # Call the LLM Model
    rewritten_query = LLMClient.run_prompt(prompt=prompt, query=query)

    return rewritten_query
