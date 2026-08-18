from langchain_core.tools import tool


# ==========================================
# Primary Tool
# ==========================================

@tool
def primary_service(message: str) -> str:
    """Primary service that intentionally fails."""

    raise RuntimeError("Primary service is unavailable.")


# ==========================================
# Fallback Tool
# ==========================================

@tool
def fallback_service(message: str) -> str:
    """Fallback service."""

    return f"Fallback successfully processed: {message}"


# ==========================================
# Fallback Logic
# ==========================================

message = "Process this request"

try:

    result = primary_service.invoke({
        "message": message
    })

    print("Primary:", result)

except Exception as e:

    print("Primary failed:", e)

    print("Using fallback...")

    result = fallback_service.invoke({
        "message": message
    })

    print("Fallback:", result)