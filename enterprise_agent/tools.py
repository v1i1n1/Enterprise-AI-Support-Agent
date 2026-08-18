import logging

import json

from enterprise_agent.rag.retriever import create_retriever

from enterprise_agent.rag.vectorstore import create_vector_store

logger = logging.getLogger("enterprise_agent.tools")


from langchain_core.tools import tool



# ==========================================
# Ticket Store
# ==========================================

tickets = {
    "INC001": {
        "ticket_id": "INC001",
        "description": "VPN issue",
        "status": "In Progress",
        "priority": "Medium"
    },

    "INC002": {
        "ticket_id": "INC002",
        "description": "Password reset",
        "status": "Resolved",
        "priority": "Low"
    },

    "INC003": {
        "ticket_id": "INC003",
        "description": "Laptop issue",
        "status": "Assigned",
        "priority": "Medium"
    }
}


ticket_counter = 4

# ==========================================
# Ticket Statistics
# ==========================================

def get_open_ticket_count():
    """Return the number of currently open tickets."""

    return sum(
        1
        for ticket in tickets.values()
        if ticket["status"] not in ["Closed", "Resolved"]
    )

# ==========================================
# Ticket Lookup
# ==========================================

@tool
def lookup_ticket(ticket_id: str) -> str:
    """Look up the details of an IT support ticket."""

    logger.info(
        "Looking up ticket: %s",
        ticket_id
    )

    ticket = tickets.get(ticket_id)

    if not ticket:

        result = {
            "error": f"Ticket {ticket_id} was not found."
        }

        logger.warning(
            "Ticket %s was not found.",
            ticket_id
        )

        return json.dumps(result)


    logger.info(
        "Ticket lookup completed: %s",
        ticket
    )

    return json.dumps(ticket)

# ==========================================
# List Tickets
# ==========================================

@tool
def list_tickets() -> str:
    """Return all support tickets raised in the current session."""

    logger.info(
        "Fetching all support tickets."
    )

    if not tickets:

        return json.dumps({
            "message": "No support tickets have been created."
        })

    ticket_list = list(tickets.values())

    logger.info(
        "Returning %s support tickets.",
        len(ticket_list)
    )

    return json.dumps(ticket_list)


# ==========================================
# Create Ticket
# ==========================================

@tool
def create_ticket(description: str) -> str:
    """Create a new IT support ticket."""

    global ticket_counter

    logger.info(
        "Creating ticket for issue: %s",
        description
    )

    ticket_id = f"INC{ticket_counter:03d}"

    ticket = {
        "ticket_id": ticket_id,
        "description": description,
        "status": "Open",
        "priority": "Medium"
    }

    tickets[ticket_id] = ticket

    ticket_counter += 1

    logger.info(
        "Ticket %s created successfully.",
        ticket_id
    )

    return json.dumps(ticket)

# ==========================================
# Close Ticket
# ==========================================

@tool
def close_ticket(ticket_id: str) -> str:
    """Close an existing IT support ticket."""

    logger.info(
        "Closing ticket: %s",
        ticket_id
    )

    ticket = tickets.get(ticket_id)

    if not ticket:

        result = {
            "error": f"Ticket {ticket_id} was not found."
        }

        logger.warning(
            "Cannot close ticket %s because it was not found.",
            ticket_id
        )

        return json.dumps(result)

    if ticket["status"] in ["Closed", "Resolved"]:

        return json.dumps({
            "message": f"Ticket {ticket_id} is already closed.",
            "ticket": ticket
        })

    ticket["status"] = "Closed"

    logger.info(
        "Ticket %s closed successfully.",
        ticket_id
    )

    return json.dumps(ticket)

# ==========================================
# Knowledge Base Search
# ==========================================
@tool
def search_knowledge_base(query: str) -> str:
    """Search the internal IT knowledge base."""

    logger.info(
        "Knowledge-base search started: %s",
        query
    )

    try:

        if not query or not query.strip():

            logger.warning(
                "Knowledge-base query was empty."
            )

            return "Error: Knowledge-base query cannot be empty."

        knowledge = {
            "vpn": (
                "For VPN issues, verify your internet connection, "
                "restart the VPN client, and reconnect."
            ),

            "password": (
                "For password issues, use the company password "
                "reset portal."
            ),

            "laptop": (
                "For laptop issues, restart the device and "
                "check network connectivity."
            )
        }

        query_lower = query.lower()

        for keyword, answer in knowledge.items():

            if keyword in query_lower:

                logger.info(
                    "Knowledge-base match found: %s",
                    keyword
                )

                return answer

        logger.info(
            "No knowledge-base match found."
        )

        return "No relevant knowledge-base article was found."

    except Exception as e:

        logger.exception(
            "Knowledge-base search failed."
        )

        return f"Knowledge-base error: {e}"

# ==========================================
# RAG Knowledge Base Search Tool
# ==========================================

@tool
def search_rag_knowledge_base(query: str) -> str:
    """
    Search the enterprise RAG knowledge base.

    The tool only answers questions belonging to topics
    explicitly covered by the enterprise knowledge base.
    """

    try:

        if not query or not query.strip():

            return (
                "OUT_OF_SCOPE: Empty knowledge-base query."
            )

        query_lower = query.lower()

        # --------------------------------------------------
        # Supported Enterprise Knowledge Topics
        # --------------------------------------------------

        supported_topics = {
            "vpn": [
                "vpn",
                "virtual private network"
            ],

            "password": [
                "password",
                "password reset",
                "forgot password",
                "reset password"
            ],

            "laptop": [
                "laptop",
                "company laptop",
                "corporate laptop"
            ],

            "email": [
                "email",
                "corporate email",
                "company email"
            ]
        }

        matched_topic = None

        for topic, keywords in supported_topics.items():

            for keyword in keywords:

                if keyword in query_lower:

                    matched_topic = topic
                    break

            if matched_topic:
                break


        # --------------------------------------------------
        # Reject Questions Outside Document Topics
        # --------------------------------------------------

        if not matched_topic:

            logger.info(
                "Query rejected: unsupported enterprise topic: %s",
                query
            )

            return (
                "OUT_OF_SCOPE: The user's question is not "
                "covered by the Enterprise IT Support knowledge base. "
                "Do not answer using general knowledge. "
                "Tell the user that you can only assist with topics "
                "covered by the Enterprise IT Support knowledge base."
            )


        # --------------------------------------------------
        # Create Vector Store
        # --------------------------------------------------

        vector_store = create_vector_store()


        # --------------------------------------------------
        # Retrieve Relevant Documents
        # --------------------------------------------------

        results = vector_store.similarity_search_with_score(
            query,
            k=2
        )

        if not results:

            return (
                "OUT_OF_SCOPE: No relevant information was found "
                "in the enterprise knowledge base."
            )


        # --------------------------------------------------
        # Validate Retrieved Content
        # --------------------------------------------------

        relevant_results = []

        for document, distance in results:

            content_lower = document.page_content.lower()

            if matched_topic in content_lower:

                relevant_results.append(
                    (document, distance)
                )


        if not relevant_results:

            return (
                "OUT_OF_SCOPE: The retrieved enterprise "
                "documentation does not directly address "
                "the user's question."
            )


        # --------------------------------------------------
        # Build Enterprise Context
        # --------------------------------------------------

        context_parts = []

        for index, (document, distance) in enumerate(
            relevant_results
        ):

            context_parts.append(
                f"Knowledge Base Result {index + 1}:\n"
                f"{document.page_content}"
            )


        context = "\n\n".join(context_parts)


        # --------------------------------------------------
        # Return ONLY Enterprise Knowledge
        # --------------------------------------------------

        return (
            "The following information was retrieved directly "
            "from the Enterprise IT Support knowledge base.\n\n"

            "IMPORTANT:\n"
            "Use ONLY the information below to answer the user.\n"
            "Do NOT use general knowledge.\n"
            "Do NOT infer additional troubleshooting steps.\n"
            "Do NOT adapt procedures from another topic.\n"
            "Do NOT invent information.\n\n"

            f"{context}"
        )


    except Exception as e:

        logger.exception(
            "RAG knowledge-base search failed."
        )

        return (
            f"RAG knowledge-base error: {e}"
        )