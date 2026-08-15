from enterprise_agent.tools import (
    lookup_ticket,
    create_ticket,
    search_knowledge_base
)


# ==========================================
# Test Ticket Lookup
# ==========================================

result = lookup_ticket.invoke({
    "ticket_id": "INC001"
})

print("Ticket Lookup:")
print(result)


# ==========================================
# Test Ticket Creation
# ==========================================

result = create_ticket.invoke({
    "description": "VPN is not connecting"
})

print("\nTicket Creation:")
print(result)


# ==========================================
# Test Knowledge Base
# ==========================================

result = search_knowledge_base.invoke({
    "query": "VPN connection problem"
})

print("\nKnowledge Base:")
print(result)

print("\n===== TEST 4: EMPTY QUERY =====")

result = search_knowledge_base.invoke({
    "query": ""
})

print(result)