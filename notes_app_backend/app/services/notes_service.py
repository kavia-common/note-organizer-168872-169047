from typing import Dict, List, Optional
from ..models.note import Note


class NotesService:
    """Service layer for managing notes in memory."""

    def __init__(self):
        # Using an in-memory store for simplicity: {id: Note}
        self._notes: Dict[int, Note] = {}
        self._next_id: int = 1

    # PUBLIC_INTERFACE
    def create_note(self, title: str, content: str, tags: Optional[List[str]] = None) -> Dict:
        """Create a new Note and return its dict representation."""
        note = Note(title=title, content=content, tags=tags or [])
        note_id = self._next_id
        self._notes[note_id] = note
        self._next_id += 1
        return note.to_dict(note_id)

    # PUBLIC_INTERFACE
    def list_notes(self, include_archived: bool = True) -> List[Dict]:
        """Return a list of notes, optionally filtering out archived notes."""
        items = []
        for nid, note in self._notes.items():
            if not include_archived and note.archived:
                continue
            items.append(note.to_dict(nid))
        return items

    # PUBLIC_INTERFACE
    def get_note(self, note_id: int) -> Optional[Dict]:
        """Get a single note by ID."""
        note = self._notes.get(note_id)
        return note.to_dict(note_id) if note else None

    # PUBLIC_INTERFACE
    def update_note(
        self,
        note_id: int,
        title: Optional[str] = None,
        content: Optional[str] = None,
        tags: Optional[List[str]] = None,
        archived: Optional[bool] = None,
    ) -> Optional[Dict]:
        """Update a note and return the updated representation."""
        note = self._notes.get(note_id)
        if not note:
            return None
        if title is not None:
            note.title = title
        if content is not None:
            note.content = content
        if tags is not None:
            note.tags = tags
        if archived is not None:
            note.archived = archived
        return note.to_dict(note_id)

    # PUBLIC_INTERFACE
    def delete_note(self, note_id: int) -> bool:
        """Delete a note by ID. Returns True if deleted."""
        if note_id in self._notes:
            del self._notes[note_id]
            return True
        return False

    # PUBLIC_INTERFACE
    def search(self, query: str) -> List[Dict]:
        """Simple search in title and content."""
        q = (query or "").lower().strip()
        if not q:
            return []
        results = []
        for nid, note in self._notes.items():
            if q in note.title.lower() or q in note.content.lower():
                results.append(note.to_dict(nid))
        return results


# Singleton instance to be used by routes
notes_service = NotesService()
