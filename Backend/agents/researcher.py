from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, ToolMessage, HumanMessage
from Backend.utils.Utils import AgentState
from langchain_tavily import TavilySearch
import json
import os
from dotenv import load_dotenv

load_dotenv()

Tavily_key = os.getenv("Tavily_Api_key")
GROQ_KEY = os.getenv("GROQ_API_KEY")

search_tool = TavilySearch(tavily_api_key=Tavily_key, max_results=3)

Model = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0.7,  
    api_key=GROQ_KEY
)

Model_with_tool = Model.bind_tools(tools=[search_tool])

def researcher_node(state: AgentState):
    last_message = state["messages"][-1]
    query = last_message.content if hasattr(last_message, 'content') else str(last_message)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a Research Agent. Your task is to gather comprehensive information.
        Use the search tool when you need current or specific information.
        Provide detailed, well-structured research findings."""),
        ("human", "Research this topic: {query}")
    ])

    formatted = prompt.format_messages(query=query)
    response = Model_with_tool.invoke(formatted)

    if hasattr(response, "tool_calls") and response.tool_calls:
        tool_call = response.tool_calls[0]
        tool_result = search_tool.invoke(tool_call["args"])
        
        tool_message = ToolMessage(
            tool_call_id=tool_call["id"],
            name=tool_call["name"],
            content=json.dumps(tool_result)
        )

        final_answer = Model_with_tool.invoke(
            formatted + [response, tool_message]
        )
        research_content = final_answer.content
    else:
        research_content = response.content
    
    # Create research message
    research_message = AIMessage(
        content=f"# 📚 RESEARCH FINDINGS\n\n{research_content}",
        metadata={"agent": "researcher"}
    )
    
    return {
        "research_content": research_content,
        "messages": state["messages"] + [research_message],
        "next": "writer"  
    }

if __name__ == "__main__":
    mock_state = {
        "messages": [HumanMessage(content="Tell me about artificial intelligence")],
        "next": "researcher",
        "revision_number": 0,
        "research_content": None,
        "final_document": None
    }
    result = researcher_node(mock_state)
    print("Research completed!")
    print(f"Content length: {len(result['research_content'])} chars")
    print(f"Next agent: {result['next']}")