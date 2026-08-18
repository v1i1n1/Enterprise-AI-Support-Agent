import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

from enterprise_agent.agent import agent
from enterprise_agent.tools import tickets, get_open_ticket_count


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Enterprise AI Support",
    page_icon="AI",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.html("""
<style>

.stApp {
    background: #f4f7fb;
}

.block-container {
    max-width: 1050px;
    padding-top: 35px;
    padding-bottom: 40px;
}


/* Header */

.main-header {
    background: linear-gradient(135deg, #111827, #243247);
    border-radius: 20px;
    padding: 30px 35px;
    margin-bottom: 25px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.10);
}

.main-title {
    color: white;
    font-size: 32px;
    font-weight: 700;
    margin: 0;
}

.main-subtitle {
    color: #d1d5db;
    font-size: 15px;
    margin-top: 8px;
}

.online-status {
    color: #86efac;
    font-size: 14px;
    font-weight: 600;
    margin-top: 15px;
}


/* Ticket statistics */

.ticket-card {
    background: white;
    border-radius: 16px;
    padding: 18px 22px;
    margin-bottom: 25px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

.ticket-label {
    color: #6b7280;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
}

.ticket-number {
    color: #111827;
    font-size: 30px;
    font-weight: 700;
    margin-top: 3px;
}

.ticket-description {
    color: #6b7280;
    font-size: 12px;
    margin-top: 2px;
}


/* Welcome */

.welcome-title {
    text-align: center;
    color: #111827;
    font-size: 28px;
    font-weight: 700;
    margin-top: 15px;
}

.welcome-subtitle {
    text-align: center;
    color: #6b7280;
    font-size: 15px;
    margin-top: 8px;
    margin-bottom: 25px;
}


/* Section */

.section-title {
    color: #374151;
    font-size: 14px;
    font-weight: 600;
    margin-top: 20px;
    margin-bottom: 10px;
}


/* RAG badge */

.rag-badge {
    display: inline-block;
    background: #ecfdf5;
    color: #047857;
    border: 1px solid #a7f3d0;
    border-radius: 20px;
    padding: 5px 11px;
    font-size: 11px;
    font-weight: 600;
    margin-top: 8px;
}


/* Footer */

.footer {
    text-align: center;
    color: #9ca3af;
    font-size: 12px;
    margin-top: 35px;
    padding-bottom: 20px;
}

</style>
""")


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# HEADER
# ============================================================

st.html("""
<div class="main-header">

    <div class="main-title">
        Enterprise AI Support
    </div>

    <div class="main-subtitle">
        AI-powered IT support using Agentic AI, RAG and enterprise knowledge.
    </div>

    <div class="online-status">
        ● Agent Online
    </div>

</div>
""")


# ============================================================
# TICKET COUNT
# ============================================================

open_ticket_count = get_open_ticket_count()

st.html(f"""
<div class="ticket-card">

    <div class="ticket-label">
        Open Support Tickets
    </div>

    <div class="ticket-number">
        {open_ticket_count}
    </div>

    <div class="ticket-description">
        Active tickets currently requiring attention
    </div>

</div>
""")


# ============================================================
# WELCOME MESSAGE
# ============================================================

if not st.session_state.messages:

    st.html("""
    <div class="welcome-title">
        How can I help you today?
    </div>

    <div class="welcome-subtitle">
        Describe your IT issue and I'll help you troubleshoot it.
    </div>
    """)


# ============================================================
# QUICK ACTIONS
# ============================================================

st.markdown(
    '<div class="section-title">Quick Actions</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)


with col1:

    vpn_clicked = st.button(
        "VPN Issue",
        use_container_width=True
    )


with col2:

    password_clicked = st.button(
        "Password Reset",
        use_container_width=True
    )


with col3:

    laptop_clicked = st.button(
        "Laptop Issue",
        use_container_width=True
    )


with col4:

    email_clicked = st.button(
        "Email Issue",
        use_container_width=True
    )


# ============================================================
# QUICK ACTION QUESTIONS
# ============================================================

selected_question = None


if vpn_clicked:

    selected_question = (
        "My corporate VPN is not connecting. What should I do?"
    )


elif password_clicked:

    selected_question = (
        "I forgot my corporate password. What should I do?"
    )


elif laptop_clicked:

    selected_question = (
        "My company laptop is having problems. What should I do?"
    )


elif email_clicked:

    selected_question = (
        "I am having problems with my corporate email. What should I do?"
    )


# ============================================================
# DISPLAY CONVERSATION
# ============================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        with st.chat_message("user"):

            st.write(message["content"])

    else:

        with st.chat_message("assistant"):

            st.markdown(message["content"])

            st.html("""
            <div class="rag-badge">
                Enterprise Knowledge
            </div>
            """)


# ============================================================
# MANUAL QUESTION INPUT
# ============================================================

st.markdown(
    '<div class="section-title">Ask Your IT Support Question</div>',
    unsafe_allow_html=True
)

input_col, button_col = st.columns([5, 1])

with input_col:

    manual_input = st.text_input(
        "Describe your IT issue",
        placeholder="Example: My VPN is not connecting...",
        label_visibility="collapsed"
    )

with button_col:

    send_clicked = st.button(
        "Send",
        use_container_width=True
    )


user_input = selected_question

if not user_input and send_clicked and manual_input.strip():

    user_input = manual_input.strip()


# ============================================================
# PROCESS USER REQUEST
# ============================================================

if user_input:

    # --------------------------------------------------------
    # Store user message
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )


    # --------------------------------------------------------
    # Display user message
    # --------------------------------------------------------

    with st.chat_message("user"):

        st.write(user_input)


    # --------------------------------------------------------
    # Call Agent
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("AI Support Agent is thinking..."):

            try:

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


            except Exception as e:

                answer = (
                    "Sorry, I encountered an error while "
                    "processing your request.\n\n"
                    f"Error: {e}"
                )


        st.markdown(answer)

        st.html("""
        <div class="rag-badge">
            Enterprise Knowledge
        </div>
        """)


    # --------------------------------------------------------
    # Store AI response
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


    # --------------------------------------------------------
    # Refresh UI
    # --------------------------------------------------------
    # This makes the ticket count immediately reflect
    # ticket creation or ticket closure.

    st.rerun()


# ============================================================
# CURRENT TICKET LIST
# ============================================================

st.markdown(
    '<div class="section-title">Current Support Tickets</div>',
    unsafe_allow_html=True
)

if tickets:

    for ticket_id, ticket in tickets.items():

        status = ticket["status"]

        if status in ["Closed", "Resolved"]:
            status_text = "Closed"
        else:
            status_text = "Open"

        st.markdown(
            f"""
            **{ticket_id}** — {ticket["description"]}  
            Status: **{status_text}** | Priority: **{ticket["priority"]}**
            """
        )

else:

    st.info("No support tickets available.")


# ============================================================
# FOOTER
# ============================================================

st.html("""
<div class="footer">
    Enterprise AI Support Agent | Agentic AI + RAG + FAISS
</div>
""")