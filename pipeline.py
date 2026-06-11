from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

def run_research_pipeline(topic: str)-> dict:
    state={}
    #search agent working
    print("\n"+"=" *50)
    print("Step 1 : Search Agent is working...")
    print("=" *50)

    search_agent=build_search_agent()
    search_result=search_agent.invoke({
        "messages":[("user", f"Find recent, reliable and detailed information about: {topic}")]
    })

    state['search_results']=search_result['messages'][-1].content
    print("\n search results", state['search_results'])

    #step 2 : reader agent working
    print("\n"+"=" *50)
    print("Step 2 : Reader Agent is working...")
    print("=" *50)
    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:800]}"
        )]
    })

    state['scraped_content'] = reader_result['messages'][-1].content

    print("\nscraped content: \n", state['scraped_content'])

    #step 3 : writer chain working
    print("\n"+"=" *50) 
    print("Step 3 : Writer is drafting report...")
    print("=" *50)

    research_combined=(
        f"Search Results:\n{state['search_results']}\n\n"
        f"Detailed Scraped Content:\n{state['scraped_content']}"
    )

    state['report']=writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("\nFinal Report:\n", state['report'])

    #critic report
    print("\n"+"=" *50)
    print("Step 4 : Critic is evaluating the report...")
    print("=" *50)
    state['feedback']=critic_chain.invoke({
        "report": state['report']
    })
    print("\nCritic Report:\n", state['feedback'])

    return state


if __name__=="__main__":
    topic=input("Enter a research topic: ")
    run_research_pipeline(topic)