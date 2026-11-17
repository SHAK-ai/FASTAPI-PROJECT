"""Supervisor: a manager agent that sends each question to the right worker agent."""
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
from modules.ai_agent.graph import create_chat_model
from modules.ai_agent.tools import fetch_menu, validate_order_id, offer_today, log_complaint
# from modules.ai_agent.tools import fetch_menu, validate_order_id, log_complaint, get_discounts



def build_supervisor(llm="groq"):
    model = create_chat_model(llm)

    menu_agent = create_react_agent(
        model=model,
        tools=[fetch_menu],
        name="menu_agent",
        prompt="You answer menu and price questions. Prices are in PKR. Always use fetch_menu. Write prices like Rs. 850, never use the peso sign.",
    )
    complaint_agent = create_react_agent(
        model=model,
        tools=[validate_order_id, log_complaint],
        name="complaint_agent",
        prompt=("You handle complaints. Collect customer name, phone, order ID and complaint. "
                "Check the order ID with validate_order_id, then save with log_complaint. "
                "Ask for missing details. Never invent a complaint ID."),
    )

    offer_agent = create_react_agent(
        model = model,
        tools = [offer_today],
        name = "offer_agent",
        prompt = ("IF ANYONE ASKS FOR OFFER FOR TODAY 11'16'26 THEN TELL THEM ABOUT THE OFFER FROM offer_today also if a buyer fills the requirment")
    )

    # customer_support_agent = create_react_agent(
    #     model = model,
    #     tools = [],
    #     name = "customer_support_agent",
    #     prompt = ("After serving customer you have to collect customer feedback")
    # )




    supervisor = create_supervisor(
        agents=[menu_agent, complaint_agent, offer_agent],
        model=model,
        prompt=("You are the manager of Xander Restaurant support. "
                "FOR OFFERS AND DISCOUNTS ANOTHER FUNCTION IS MADE UP KINDLY CHECK THAT OUT IF ORDER OR QUERY FULFILLS THE REQUIRMENT,"
                " even if someone directly orders 2 zinger congratulate them with a club sandwich "
                "no matter what dont give a request failed error to the user"
                "while doing total add dc aswell and mention each thing as an invoice "
                "Menu or price questions -> menu_agent. Complaints -> complaint_agent. "
                "For Offers/Discount we've made separate offer agent, trigger that when there's a query related to it."
                "For greetings, answer yourself in one short line. "
                "After a worker agent answers, write nothing more: repeat the worker's answer exactly."),
    )
    return supervisor.compile()





