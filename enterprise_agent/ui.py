import streamlit as st

from enterprise_agent.agent import agent


st.set_page_config(
    page_title="Enterprise AI Support",
    page_icon="🤖"
)

st.title("🤖 Enterprise AI Support Agent")

st.write(
    "Ask questions about IT troubleshooting, "
    "tickets, and enterprise support."
)


user_input = st.chat_input(
    "Describe your IT issue..."
)


if user_input:

    st.chat_message("user").write(user_input)

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        },
        config={
            "configurable": {
                "thread_id": "streamlit-user"
            }
        }
    )

    answer = response["messages"][-1].content

    with st.chat_message("assistant"):
        st.write(answer)
        