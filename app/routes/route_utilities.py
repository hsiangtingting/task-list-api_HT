from flask import Blueprint, abort, make_response, request, Response
from ..db import db

def validate_model(cls, id):
    try:
        id = int(id)
    except:
        # Match the expected error message format used in tests (e.g. "task 1 invalid")
        invalid = {"message": f"{cls.__name__.lower()} {id} invalid"}
        abort(make_response(invalid, 400))

    query = db.select(cls).where(cls.id==id)
    model = db.session.scalar(query)
    if not model:
        # Match expected error message format used in tests (e.g. "task 1 not found")
        not_found = {"message": f"{cls.__name__.lower()} {id} not found"}
        abort(make_response(not_found, 404))

    return model

