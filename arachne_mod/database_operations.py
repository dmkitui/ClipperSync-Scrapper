from models import ClipperData, db_connect, create_clipperdata_table, ClipperDataSchema
from sqlalchemy import desc
from sqlalchemy.orm import sessionmaker

engine = db_connect()
create_clipperdata_table(engine)
session = sessionmaker(bind=engine)()

data_schema = ClipperDataSchema()


def fetch_data():
    raw_data = session.query(ClipperData).order_by(desc('date')).all()
    session.close()
    json_output = data_schema.dump(raw_data, many=True)
    return json_output


def edit_note(note_id, edited_note):
    print('Edit note ID: ', note_id)

    note = session.query(ClipperData).filter_by(id=note_id).first()
    if not note:
        return 'Specified note does not exist', 404

    note_to_edit = data_schema.dump(note).data
    current_note = note_to_edit['raw_note'] if note_to_edit['edit_flag'] is False else note_to_edit['edited_note']

    if edited_note == current_note:
        return 'Current note is same as current', 409

    note.edited_note = edited_note
    note.edit_flag = True
    session.commit()
    session.close()

    return True, 201
