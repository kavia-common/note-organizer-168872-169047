# PUBLIC_INTERFACE
class Note:
    """A simple Note domain model for the Notes App."""

    def __init__(self, title: str, content: str, tags=None):
        self.title = title
        self.content = content
        self.tags = tags or []
        self.archived = False

    def to_dict(self, note_id: int):
        """Convert this Note to a dictionary including the provided ID."""
        return {
            "id": note_id,
            "title": self.title,
            "content": self.content,
            "tags": self.tags,
            "archived": self.archived,
        }
