from langchain_core.tools import tool


attempt_count = 0


@tool
def unreliable_tool(message: str) -> str:
    """Simulates a tool that may temporarily fail."""

    global attempt_count

    attempt_count += 1

    print(f"Attempt {attempt_count}")

    # Fail first two attempts
    if attempt_count < 3:
        raise RuntimeError("Temporary service failure")

    return f"Success: {message}"


# ==========================================
# Retry Logic
# ==========================================

max_retries = 3

for attempt in range(1, max_retries + 1):

    try:

        result = unreliable_tool.invoke({
            "message": "Process this request"
        })

        print(result)
        break

    except Exception as e:

        print(f"Error: {e}")

        if attempt == max_retries:

            print("All retry attempts failed.")

        else:

            print("Retrying...")