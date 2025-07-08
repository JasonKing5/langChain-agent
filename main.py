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

# Create the agent
memory = MemorySaver()

# 初始化聊天模型
try:
    model = init_chat_model("deepseek:deepseek-chat")  # or "openai:gpt-3.5-turbo"
except Exception as e:
    print(f"Error initializing chat model: {e}")
    print("Please make sure you have set a valid OPENAI_API_KEY")
    exit(1)

search = TavilySearch(max_results=2)
tools = [search]
agent_executor = create_react_agent(model, tools, checkpointer=memory)


# Use the agent
config = {"configurable": {"thread_id": "abc123"}}

input_message = {
    "role": "user",
    "content": "Hi, I'm Bob and I life in SF.",
}
for step in agent_executor.stream(
    {"messages": [input_message]}, config, stream_mode="values"
):
    step["messages"][-1].pretty_print()


input_message = {
    "role": "user",
    "content": "What's the weather where I live?",
}

for step in agent_executor.stream(
    {"messages": [input_message]}, config, stream_mode="values"
):
    step["messages"][-1].pretty_print()