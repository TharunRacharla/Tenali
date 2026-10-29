import tempfile
import webbrowser
from pathlib import Path


def run_notepad(note_content):
    """Write a note to a temporary text file and open it in the default browser."""
    note_content = note_content.strip()
    if not note_content:
        raise ValueError("Note content is required.")

    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        suffix=".txt",
        delete=False,
    ) as note_file:
        note_file.write(note_content)
        note_path = Path(note_file.name)

    if not webbrowser.open(note_path.as_uri()):
        raise RuntimeError("The default browser could not open the note.")
    return "Note opened."
