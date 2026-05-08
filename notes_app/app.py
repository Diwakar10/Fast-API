from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# ----------------------
# Data Model
# ----------------------
class Note(BaseModel):
    id: int
    title: str
    content: str

class NoteCreate(BaseModel):
    title: str
    content: str


# ----------------------
# In-memory storage
# ----------------------
notes: List[Note] = []


# ----------------------
# Create Note
# ----------------------
@app.post("/notes", response_model=Note)
def create_note(note: NoteCreate):
    new_id = len(notes) + 1
    new_note = Note(id=new_id, **note.dict())
    notes.append(new_note)
    return new_note


# ----------------------
# Read All Notes
# ----------------------
@app.get("/notes", response_model=List[Note])
def get_notes():
    return notes


# ----------------------
# Update Note
# ----------------------
@app.put("/notes/{note_id}", response_model=Note)
def update_note(note_id: int, updated_note: NoteCreate):
    for index, note in enumerate(notes):
        if note.id == note_id:
            notes[index] = Note(id=note_id, **updated_note.dict())
            return notes[index]
    
    raise HTTPException(status_code=404, detail="Note not found")


# ----------------------
# Delete Note
# ----------------------
@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    for index, note in enumerate(notes):
        if note.id == note_id:
            deleted_note = notes.pop(index)
            return {"message": "Deleted successfully", "note": deleted_note}
    
    raise HTTPException(status_code=404, detail="Note not found")