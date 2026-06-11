from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from tools import web_search, scrape_url
import os
from dotenv import load_dotenv

load_dotenv()

# ── Model Setup ──────────────────────────────────────────────────────────────
llm = ChatGroq(
    model="llama3-8b-8192",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

# ── Search Agent ─────────────────────────────────────────────────────────────
def build_search_agent():
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm, [web_search], prompt)
    return AgentExecutor(agent=agent, tools=[web_search], verbose=True, handle_parsing_errors=True)

# ── Reader Agent ─────────────────────────────────────────────────────────────
def build_reader_agent():
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm, [scrape_url], prompt)
    return AgentExecutor(agent=agent, tools=[scrape_url], verbose=True, handle_parsing_errors=True)

# ── Writer Chain ─────────────────────────────────────────────────────────────
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()

# ── Critic Chain ─────────────────────────────────────────────────────────────
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()