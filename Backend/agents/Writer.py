from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from Backend.utils.Utils import AgentState
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

Model = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0.8,
    api_key=GROQ_API_KEY
)

def writer_node(state: AgentState):
    research_text = state.get("research_content", "")
    
    if not research_text:
        for msg in reversed(state["messages"]):
            if isinstance(msg, AIMessage) and "RESEARCH" in msg.content:
                research_text = msg.content
                break
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a professional Writer Agent. 
        Transform the research into a well-structured, engaging document.
        
        Guidelines:
        1. Create clear headings and sections
        2. Write in a professional yet engaging tone
        3. Expand on key points from research
        4. Add original insights where appropriate
        5. Ensure logical flow from introduction to conclusion
        
        Your output should be publication-ready."""),
        ("human", "Research to write about:\n{research}")
    ])
    
    chain = prompt | Model
    final_document = chain.invoke({"research": research_text[:5000]})  
    
    writer_message = AIMessage(
        content=f"# FINAL DOCUMENT\n\n{final_document.content}",
        metadata={"agent": "writer", "revision": state.get("revision_number", 0)}
    )
    
    return {
        "final_document": final_document.content,
        "messages": state["messages"] + [writer_message],
        "next": "critiquer"  
    }

if __name__ == "__main__":
    mock_state = {
        "messages": [AIMessage(content="# RESEARCH\nAI is transforming technology.")],
        "next": "writer",
        "revision_number": 0,
        "research_content": "Artificial Intelligence is revolutionizing industries from healthcare to finance. Recent advances in machine learning have enabled breakthroughs in natural language processing and computer vision.",
        "final_document": None
    }
    result = writer_node(mock_state)
    print("Writing completed!")
    print(result)
    print(f"Document length: {len(result['final_document'])} chars")
    print(f"Next agent: {result['next']}")