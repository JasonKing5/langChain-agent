# Import relevant functionality
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 检查必要的环境变量
required_vars = ["OPENAI_API_KEY", "OPENAI_API_BASE_URL", "TAVILY_API_KEY"]
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    print(f"错误：缺少必要的环境变量: {', '.join(missing_vars)}")
    print("请确保 .env 文件已正确配置")
    exit(1)

# 设置环境变量
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_BASE_URL"] = os.getenv("OPENAI_API_BASE_URL")
os.environ["DEEPSEEK_API_KEY"] = os.getenv("DEEPSEEK_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_TRACING"] = os.getenv("LANGSMITH_TRACING")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# 初始化聊天模型
try:
    model = init_chat_model("deepseek:deepseek-chat") # or init_chat_model("gemini-2.0-flash", model_provider="google_genai")
except Exception as e:
    print(f"Error initializing chat model: {e}")
    print("Please make sure you have set a valid LLM API_KEY")
    exit(1)

# Use the agent
# query = "Hi!"

# query = "Search for the weather in SF!"
# model_with_tools = model.bind_tools(tools)
# response = model_with_tools.invoke([{"role": "user", "content": query}])
# print('response text:', response.text())
# print('tool calls:', response.tool_calls)

search = TavilySearch(max_results=2)
tools = [search]

# Create the agent
memory = MemorySaver()

agent_executor = create_react_agent(model, tools, checkpointer=memory)

config = {"configurable": {"thread_id": "abc123"}}

# input_message = {"role": "user", "content": "Hi!"}
input_message = {"role": "user", "content": "Search for the weather in SF!"}
# response = agent_executor.invoke({"messages": [input_message]})

# for message in response["messages"]:
#     message.pretty_print()

# for step in agent_executor.stream({"messages": [input_message]}, stream_mode="values"):
#     step["messages"][-1].pretty_print()

# for step, metadata in agent_executor.stream(
#     {"messages": [input_message]}, stream_mode="messages"
# ):
#     if metadata["langgraph_node"] == "agent" and (text := step.text()):
#         print(text, end="|")

input_message = {"role": "user", "content": "Hi, I'm Bob!"}
for step in agent_executor.stream({"messages": [input_message]}, config, stream_mode="values"):
    step["messages"][-1].pretty_print()

input_message = {"role": "user", "content": "What's my name?"}
for step in agent_executor.stream(
    {"messages": [input_message]}, config, stream_mode="values"
):
    step["messages"][-1].pretty_print()

input_message = {"role": "user", "content": "What's my name?"}
config = {"configurable": {"thread_id": "abc124"}}
for step in agent_executor.stream(
    {"messages": [input_message]}, config, stream_mode="values"
):
    step["messages"][-1].pretty_print()