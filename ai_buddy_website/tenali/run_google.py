import re
import webbrowser
from urllib.parse import quote_plus


def run_google(user_input):
    """Open Google or search for the query provided by the caller."""
    search_query = re.sub(
        r"\b(?:open google|google search|google)\b",
        "",
        user_input,
        flags=re.IGNORECASE,
    ).strip()
    if search_query:
        url = f"https://www.google.com/search?q={quote_plus(search_query)}"
        message = f"Searching Google for {search_query}."
    else:
        url = "https://www.google.com"
        message = "Opening Google."

    if not webbrowser.open(url):
        raise RuntimeError("The default browser could not be opened.")
    return message
