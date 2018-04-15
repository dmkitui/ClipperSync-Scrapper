from models import ClipperData, db_connect, create_clipperdata_table
from sqlalchemy import desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.serializer import loads, dumps

engine = db_connect()
create_clipperdata_table(engine)
session = sessionmaker(bind=engine)()

def fetch_data():
    data = session.query(ClipperData).order_by(desc('date')).all()
    session.close()

    raw_data = [d.__dict__ for d in data]
    return [{'id':x['id'], 'date': x['date'], 'note': x['note']} for x in raw_data]

def edit_note(note_id, edited_note):
    print('Edit note ID: ', note_id)

    note_to_edit = session.query(ClipperData).filter_by(id=note_id).first()

    if not note_to_edit:
        return 'Note Does Not Exist', 404

    note_to_edit = note_to_edit.__dict__
    current_note = note_to_edit['note']

    print('Note to edit: ', note_to_edit, 'proposed edit: ', edited_note, 'Current: ', current_note)

    if edited_note == current_note:
        return 'Current note is same as current', 409

    return None, 500
