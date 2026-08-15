import logging

from enterprise_agent.rag.retriever import create_retriever

logger = logging.getLogger("enterprise_agent.tools")


from langchain_core.tools import tool


# ==========================================
# Ticket Lookup
# ==========================================

@tool
def lookup_ticket(ticket_id: str) -> str:
    """Look up the status of an IT support ticket."""

    logger.info(
        "Looking up ticket: %s",
        ticket_id
    )

    tickets = {
        "INC001": "VPN issue - In Progress",
        "INC002": "Password reset - Resolved",
        "INC003": "Laptop issue - Assigned"
    }

    result = tickets.get(
        ticket_id,
        f"Ticket {ticket_id} was not found."
    )

    logger.info(
        "Ticket lookup completed: %s",
        result
    )

    return result


# ==========================================
# Create Ticket
# ==========================================

@tool
def create_ticket(description: str) -> str:
    """Create a new IT support ticket."""

    logger.info(
        "Creating ticket for issue: %s",
        description
    )

    result = (
        f"Ticket created successfully for issue: "
        f"{description}"
    )

    logger.info("Ticket creation completed.")

    return result


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
    """Search the enterprise RAG knowledge base for detailed IT procedures, troubleshooting, and policies."""

    try:

        if not query or not query.strip():
            return "Error: RAG query cannot be empty."

        retriever = create_retriever()

        documents = retriever.invoke(query)

        if not documents:
            return (
                "No relevant information was found "
                "in the enterprise knowledge base."
            )

        context_parts = []

        for index, document in enumerate(documents):

            context_parts.append(
                f"Knowledge Base Result {index + 1}:\n"
                f"{document.page_content}"
            )

        context = "\n\n".join(context_parts)

        return (
            "The following information was retrieved "
            "from the enterprise knowledge base. "
            "Use this information to answer the user's "
            "question accurately and completely. "
            "Do not omit relevant troubleshooting steps.\n\n"
            f"{context}"
        )

    except Exception as e:

        return f"RAG knowledge-base error: {e}"