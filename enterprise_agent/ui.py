import streamlit as st

from enterprise_agent.agent import agent


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Enterprise AI Support",
    page_icon="🤖",
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

    .main-header {
        background: linear-gradient(135deg, #111827, #243247);
        border-radius: 20px;
        padding: 30px 35px;
        margin-bottom: 30px;
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

    .section-title {
        color: #374151;
        font-size: 14px;
        font-weight: 600;
        margin-top: 20px;
        margin-bottom: 8px;
    }

    .rag-badge {
        display: inline-block;
        background: #ecfdf5;
        color: #047857;
        border: 1px solid #a7f3d0;
        border-radius: 20px;
        padding: 6px 12px;
        font-size: 12px;
        font-weight: 600;
        margin-top: 8px;
    }

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
    <div class="main-title">🤖 Enterprise AI Support</div>
    <div class="main-subtitle">
        AI-powered IT support using Agentic AI, RAG and enterprise knowledge.
    </div>
    <div class="online-status">● Agent Online</div>
</div>
""")


# ============================================================
# WELCOME
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

col1, col2, col3, col4 = st.columns(4)


with col1:
    vpn_clicked = st.button(
        "🌐 VPN",
        use_container_width=True
    )


with col2:
    password_clicked = st.button(
        "🔐 Password",
        use_container_width=True
    )


with col3:
    laptop_clicked = st.button(
        "💻 Laptop",
        use_container_width=True
    )


with col4:
    email_clicked = st.button(
        "📧 Email",
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
        "I forgot my corporate password. How can I reset it?"
    )


elif laptop_clicked:

    selected_question = (
        "My company laptop is not working. What should I do?"
    )


elif email_clicked:

    selected_question = (
        "I am having problems with my corporate email."
    )


# ============================================================
# CHAT HISTORY
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
                📚 Enterprise Knowledge
            </div>
            """)


# ============================================================
# CHAT INPUT
# ============================================================

chat_input = st.chat_input(
    "Describe your IT issue..."
)


user_input = selected_question or chat_input


# ============================================================
# PROCESS USER REQUEST
# ============================================================

if user_input:

    # Store user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Display user message
    with st.chat_message("user"):

        st.write(user_input)


    # Call Agent
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
            📚 Enterprise Knowledge
        </div>
        """)


    # Store AI response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


# ============================================================
# FOOTER
# ============================================================

st.html("""
<div class="footer">
    Enterprise AI Support • Agentic AI • RAG • FAISS • LangChain
</div>
""")