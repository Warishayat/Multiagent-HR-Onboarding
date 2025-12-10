from langgraph.graph import  START,StateGraph, END
from critiquer import critiquer_node
from supervisor import supervisor_node
from researcher import researcher_node
from Writer import writer_node
from Backend.utils.Utils import AgentState

state = StateGraph(AgentState)
state.add_node("Supervisor_node",supervisor_node)
state.add_node("critiquer_node",critiquer_node)
state.add_node("Writer_node",writer_node)
state.add_node('reseacher_node',researcher_node)




if __name__ == "__main__":
    print('Hello ray?????')