from langchain_groq import ChatGroq


class LLMClient:
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.6, max_retries=2)

    @staticmethod
    def run_prompt(prompt, query, context=None):
        # Create a chain composing prompt & llm
        chain = prompt | LLMClient.llm

        # Invoke chain
        answer = chain.invoke({"query": query, "context": context})

        return answer.content
