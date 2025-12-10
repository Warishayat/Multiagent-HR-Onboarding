# Backend/agents/supervisor.py
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from Backend.utils.Utils import AgentState, RoutingDecision
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0.1,
    api_key=GROQ_API_KEY
    )
structured_model = llm.with_structured_output(RoutingDecision)


def supervisor_node(state: AgentState):
    """
    Supervisor node - Only does INITIAL routing based on user query
    Returns: Updated state with 'next' field set to the agent to route to
    """
    user_message = state['messages'][-1].content
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are the INITIAL ROUTER. Based on the user's FIRST request, decide which agent should start.
        
        Available Agents:
        1. **researcher** - When user wants to gather information, research topics, find data
        2. **writer** - When user wants to create content, write articles, generate text
        3. **critiquer** - When user wants to review/analyze existing content
        
        Examples:
        - "Write about AI" → writer
        - "Research climate change" → researcher  
        - "Review this article" → critiquer
        
        Return ONLY the agent name."""),
        ("human", "User request: {query}")
    ])
    
    try:
        result = structured_model.invoke(prompt.format(query=user_message))
        print(result.next_agent)
        print(result.reason)
        if result is not None:
            return {
            "next": result.next_agent,
            "messages": [],
            "routing_reason":result.reason  
        }
    except Exception as e:
        print(f"[Supervisor Error] {e}")




if __name__ == "__main__":
    query = "write some letast research on ai and write 5000 words essay"
    mock_state = {
        "messages":[HumanMessage(content=query)],
        "next": "supervisor",
        "revision_number": 0
    }
    supervisor_node(mock_state)