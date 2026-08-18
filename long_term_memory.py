import sqlite3

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver


# ============================================
# Load environment variables
# ============================================

load_dotenv()


# ============================================
# User Profile Database
# ============================================

connection = sqlite3.connect("user_profiles.db")


connection.execute("""
CREATE TABLE IF NOT EXISTS user_profile (
    user_id TEXT PRIMARY KEY,
    name TEXT,
    favorite_language TEXT,
    interests TEXT
)
""")


connection.commit()


# ============================================
# Save User Profile
# ============================================

def save_profile(
    user_id,
    name=None,
    favorite_language=None,
    interests=None
):

    existing = connection.execute(
        "SELECT * FROM user_profile WHERE user_id = ?",
        (user_id,)
    ).fetchone()


    if existing:

        connection.execute("""
            UPDATE user_profile
            SET
                name = COALESCE(?, name),
                favorite_language = COALESCE(?, favorite_language),
                interests = COALESCE(?, interests)
            WHERE user_id = ?
        """, (
            name,
            favorite_language,
            interests,
            user_id
        ))

    else:

        connection.execute("""
            INSERT INTO user_profile
            (
                user_id,
                name,
                favorite_language,
                interests
            )
            VALUES (?, ?, ?, ?)
        """, (
            user_id,
            name,
            favorite_language,
            interests
        ))


    connection.commit()


# ============================================
# Get User Profile
# ============================================

def get_profile(user_id):

    result = connection.execute(
        """
        SELECT
            name,
            favorite_language,
            interests
        FROM user_profile
        WHERE user_id = ?
        """,
        (user_id,)
    ).fetchone()


    if not result:
        return None


    return {
        "name": result[0],
        "favorite_language": result[1],
        "interests": result[2]
    }


# ============================================
# Create LLM
# ============================================

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


# ============================================
# Persistent Conversation Memory
# ============================================

with SqliteSaver.from_conn_string(
    "conversation_memory.db"
) as checkpointer:


    # ========================================
    # Create Agent
    # ========================================

    agent = create_agent(

        model=llm,

        tools=[],

        system_prompt="""
You are a helpful personal AI assistant.

Use the user profile information provided
in the conversation when it is relevant.

Answer questions clearly and naturally.

Do not invent information about the user.
""",

        checkpointer=checkpointer
    )


    # ========================================
    # User / Session Configuration
    # ========================================

    user_id = "user-1"

    config = {
        "configurable": {
            "thread_id": "conversation-1"
        }
    }


    # ========================================
    # Welcome Message
    # ========================================

    print()
    print("====================================")
    print("      LONG-TERM MEMORY CHATBOT")
    print("====================================")
    print("Type 'exit' to stop.")
    print()


    # ========================================
    # Chat Loop
    # ========================================

    while True:

        user_input = input("You: ").strip()


        # ------------------------------------
        # Exit
        # ------------------------------------

        if user_input.lower() == "exit":

            print("AI: Goodbye!")

            break


        # ------------------------------------
        # Ignore empty input
        # ------------------------------------

        if not user_input:

            print("AI: Please enter a message.")
            print()

            continue


        # ====================================
        # Profile Extraction
        # ====================================

        lower_input = user_input.lower()


        # ------------------------------------
        # Name
        # ------------------------------------

        if lower_input.startswith("my name is"):

            name = user_input[
                len("my name is"):
            ].strip()


            if name:

                save_profile(
                    user_id=user_id,
                    name=name
                )


        # ------------------------------------
        # Favorite Programming Language
        # ------------------------------------

        elif lower_input.startswith(
            "my favorite programming language is"
        ):

            language = user_input[
                len(
                    "my favorite programming language is"
                ):
            ].strip()


            if language:

                save_profile(
                    user_id=user_id,
                    favorite_language=language
                )


        # ------------------------------------
        # British spelling: Favourite
        # ------------------------------------

        elif lower_input.startswith(
            "my favourite programming language is"
        ):

            language = user_input[
                len(
                    "my favourite programming language is"
                ):
            ].strip()


            if language:

                save_profile(
                    user_id=user_id,
                    favorite_language=language
                )


        # ------------------------------------
        # Interest
        # ------------------------------------

        elif lower_input.startswith(
            "i am interested in"
        ):

            interest = user_input[
                len("i am interested in"):
            ].strip()


            if interest:

                save_profile(
                    user_id=user_id,
                    interests=interest
                )


        # ------------------------------------
        # Interest - Short Form
        # ------------------------------------

        elif lower_input.startswith(
            "i'm interested in"
        ):

            interest = user_input[
                len("i'm interested in"):
            ].strip()


            if interest:

                save_profile(
                    user_id=user_id,
                    interests=interest
                )


        # ====================================
        # Retrieve User Profile
        # ====================================

        profile = get_profile(user_id)


        profile_text = ""


        if profile:

            profile_text = f"""
User Profile:

Name: {profile["name"]}

Favorite Programming Language:
{profile["favorite_language"]}

Interests:
{profile["interests"]}
"""


        # ====================================
        # Send Request to Agent
        # ====================================

        response = agent.invoke(

            {
                "messages": [
                    {
                        "role": "user",

                        "content": f"""
{profile_text}

Current User Message:
{user_input}
"""
                    }
                ]
            },

            config
        )


        # ====================================
        # Display AI Response
        # ====================================

        print()

        print(
            "AI:",
            response["messages"][-1].content
        )

        print()