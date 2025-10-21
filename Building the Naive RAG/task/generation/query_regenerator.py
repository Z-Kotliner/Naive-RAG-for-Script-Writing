from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


def rewrite_query(query) -> str:
    # Instantiate the llm with model
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.6,
        max_retries=2)

    # Create messages
    messages = [
        ("human",
         """You are a helpful AI assistant that re-writes user user query to improve search precision. \n
          The context of the application is about searching movie scripts.
          The re-written query will be used to perform similarity search on a vector store that contains all scenes in the script. \n
          
          Make sure the query emphasis crucial keywords of the input for good scene retrieval.
          
          Respond only with the re-written query and nothing else. Do not put options with 'or'.
          
          Example:
          
          input - "Only scenes involving trains"
          output - "Find scenes featuring trains"
          
    
         """
         ),
        ("user", "{input}")
    ]

    # Create a prompt
    prompt = ChatPromptTemplate.from_messages(messages)

    # Create a chain composing prompt & llm
    chain = prompt | llm

    # Invoke chain
    rewritten_query = chain.invoke({"input": query})

    return rewritten_query.content
