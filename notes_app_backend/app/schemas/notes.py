from marshmallow import Schema, fields, validate


class NoteBaseSchema(Schema):
    title = fields.Str(required=True, description="Title of the note", validate=validate.Length(min=1, max=200))
    content = fields.Str(required=True, description="Content/body of the note")
    tags = fields.List(fields.Str(), required=False, description="List of tags (strings)")
    archived = fields.Bool(required=False, load_default=False, description="Archive status")


class NoteCreateSchema(NoteBaseSchema):
    """Schema for creating a note."""


class NoteUpdateSchema(Schema):
    title = fields.Str(required=False, description="Updated title of the note", validate=validate.Length(min=1, max=200))
    content = fields.Str(required=False, description="Updated content/body of the note")
    tags = fields.List(fields.Str(), required=False, description="Updated list of tags")
    archived = fields.Bool(required=False, description="Updated archive status")


class NoteResponseSchema(NoteBaseSchema):
    id = fields.Int(required=True, description="Unique identifier of the note")


class NotesListResponseSchema(Schema):
    items = fields.List(fields.Nested(NoteResponseSchema), required=True, description="List of notes")
    total = fields.Int(required=True, description="Total count of notes in this response")
