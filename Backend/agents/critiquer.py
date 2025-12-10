import os
from typing import Literal, List
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
from Backend.utils.Utils import AgentState
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="qwen/qwen3-32b", temperature=0.1, api_key=GROQ_API_KEY)

class CritiqueDecision(BaseModel):
    decision: Literal["APPROVE", "REVISE"]
    score: int = Field(ge=1, le=10)
    feedback: str
    improvements: List[str]

structured_llm = llm.with_structured_output(CritiqueDecision)

def critiquer_node(state: AgentState):
    rev = state.get("revision_number", 0)
    max_rev = state.get("max_revisions", 3)
    
    if rev >= max_rev:
        return {
            "messages": state["messages"] + [SystemMessage(content="Forced approval")],
            "next": "archiver",
            "revision_number": rev,
            "critique_score": 5,
            "status": "forced"
        }
    
    doc = state.get("final_document", "")
    if not doc and state["messages"]:
        doc = str(state["messages"][-1])
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Evaluate document. Return decision, score 1-10, feedback, improvements."),
        ("human", "Doc: {doc}")
    ])
    
    try:
        critique = structured_llm.invoke(prompt.format(doc=doc[:3000]))
    except:
        critique = CritiqueDecision(decision="REVISE", score=5, feedback="Error", improvements=["Fix"])
    
    if critique.decision == "APPROVE":
        return {
            "messages": state["messages"] + [SystemMessage(content=f"Approved. Score: {critique.score}")],
            "next": "archiver",
            "revision_number": rev,
            "critique_score": critique.score,
            "status": "approved"
        }
    else:
        new_rev = rev + 1
        return {
            "messages": state["messages"] + [SystemMessage(content=f"Revise. Score: {critique.score}")],
            "next": "writer",
            "revision_number": new_rev,
            "critique_score": critique.score,
            "status": "revise"
        }

if __name__ == "__main__":
    from langchain_core.messages import AIMessage
    test_state = {
    "messages": [
        AIMessage(content="# FINAL DOCUMENT\nAI good. Helps people. Many use."),
    ],
    "next": "critiquer",
    "revision_number": 0,
    "max_revisions": 3,
    "final_document": "AI good. Helps people. Many use.",
    "research_content": ""
}

    result = critiquer_node(test_state)
    print("Result:", result)