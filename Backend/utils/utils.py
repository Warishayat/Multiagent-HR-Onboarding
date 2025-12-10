# Backend/utils/Utils.py
from typing import TypedDict, List, Annotated, Literal,Optional
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    next: str  
    revision_number: int
    research_content : Optional[str]
    final_document : Optional[str]
    max_revisions: int = 3  

class RoutingDecision(BaseModel):
    next_agent: Literal['researcher', 'writer', 'critiquer', 'archiver', 'finish'] = Field(
        description="Which agent should handle this next?"
    )
    reason: str = Field(description="Brief reason for this routing decision")


class CritiqueDecision(BaseModel):
    decision: Literal["APPROVE", "REVISE"] = Field(description="APPROVE if ready for archive, REVISE if needs improvement")
    score: int = Field(description="Quality score 1-10", ge=1, le=10)
    feedback: str = Field(description="Specific actionable feedback")
    improvements: List[str] = Field(description="List of specific improvements needed")