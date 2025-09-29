from flask.views import MethodView
from flask_smorest import Blueprint
from webargs import fields
from webargs.flaskparser import use_args

from ..services.notes_service import notes_service
from ..schemas.notes import (
    NoteCreateSchema,
    NoteUpdateSchema,
    NoteResponseSchema,
    NotesListResponseSchema,
)
from ..utils.responses import success, error

blp = Blueprint(
    "Notes",
    "notes",
    url_prefix="/notes",
    description="Endpoints for managing notes (Ocean Professional theme).",
)


@blp.route("")
class NotesCollection(MethodView):
    @blp.doc(
        summary="List notes",
        description="Retrieve all notes in the system. Optionally exclude archived notes.",
        operationId="listNotes",
        tags=["Notes"],
        responses={200: NotesListResponseSchema},
    )
    @use_args({"include_archived": fields.Bool(load_default=True)}, location="query")
    def get(self, args):
        """List all notes with optional archived filter."""
        include_archived = args.get("include_archived", True)
        items = notes_service.list_notes(include_archived=include_archived)
        return success("Notes fetched successfully", data={"items": items, "total": len(items)})

    @blp.doc(
        summary="Create a note",
        description="Create a new note with title, content, and optional tags.",
        operationId="createNote",
        tags=["Notes"],
        responses={201: NoteResponseSchema},
    )
    @blp.arguments(NoteCreateSchema)
    def post(self, json_data):
        """Create a new note."""
        title = json_data.get("title")
        content = json_data.get("content")
        tags = json_data.get("tags") or []
        if not title or not content:
            return error("Title and content are required.", status_code=400)
        created = notes_service.create_note(title=title, content=content, tags=tags)
        return success("Note created successfully", data=created, status_code=201)


@blp.route("/<int:note_id>")
class NotesResource(MethodView):
    @blp.doc(
        summary="Get a note",
        description="Retrieve a single note by its ID.",
        operationId="getNote",
        tags=["Notes"],
        responses={200: NoteResponseSchema, 404: {"description": "Note not found"}},
    )
    def get(self, note_id: int):
        """Get a note by ID."""
        note = notes_service.get_note(note_id)
        if not note:
            return error("Note not found", status_code=404)
        return success("Note fetched successfully", data=note)

    @blp.doc(
        summary="Update a note",
        description="Update attributes of a note. Partial update is supported.",
        operationId="updateNote",
        tags=["Notes"],
        responses={200: NoteResponseSchema, 404: {"description": "Note not found"}},
    )
    @blp.arguments(NoteUpdateSchema)
    def put(self, json_data, note_id: int):
        """Update a note by ID (full/partial)."""
        updated = notes_service.update_note(
            note_id=note_id,
            title=json_data.get("title"),
            content=json_data.get("content"),
            tags=json_data.get("tags"),
            archived=json_data.get("archived"),
        )
        if not updated:
            return error("Note not found", status_code=404)
        return success("Note updated successfully", data=updated)

    @blp.doc(
        summary="Delete a note",
        description="Delete a note by its ID.",
        operationId="deleteNote",
        tags=["Notes"],
        responses={204: {"description": "Note deleted"}, 404: {"description": "Note not found"}},
    )
    def delete(self, note_id: int):
        """Delete a note by ID."""
        deleted = notes_service.delete_note(note_id)
        if not deleted:
            return error("Note not found", status_code=404)
        # 204 no content, but keep theme meta via message with 200 if preferred. We'll do 204 per REST.
        return success("Note deleted successfully", data=None, status_code=204)


@blp.route("/search")
class NotesSearch(MethodView):
    @blp.doc(
        summary="Search notes",
        description="Search notes by query string in title and content.",
        operationId="searchNotes",
        tags=["Notes"],
        responses={200: NotesListResponseSchema},
    )
    @use_args({"q": fields.Str(required=True)}, location="query")
    def get(self, args):
        """Search notes by a simple query string."""
        q = args.get("q", "")
        results = notes_service.search(q)
        return success("Search completed", data={"items": results, "total": len(results)})
