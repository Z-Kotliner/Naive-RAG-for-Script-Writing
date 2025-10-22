from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from .llm_service import LLMClient

# Define the prompt template
template = """
            You are a helpful AI assistant -- an expert on movie scripts. \n
            
            You will give detailed answer to the following user question
            {query}.
            
            
            Use the following scenes as context.\n
            {context}
    
            Respond within the context. Only respond with the final answer. Do not add text such as 'Here is ...' 
         """


def generate_answer(query, documents) -> str:
    # Reformat context Documents into single string
    context = "\n\n".join([document.page_content for document in documents])

    # Generate the prompt
    prompt = PromptTemplate(input_variables=["query", "context"], template=template)

    # Call the LLM Model
    answer = LLMClient.run_prompt(prompt, query, context)

    return answer
