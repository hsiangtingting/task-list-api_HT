from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from app.models.goal import Goal
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

def create_model(cls, data_dict):
    '''
    Create a model instance from a dictionary
    '''
    try:
        new_model = cls.from_dict(data_dict)
    except KeyError as e:
        response = {"details": f"Invalid data: missing {e.args[0]}"}
        abort(make_response(response, 400))

    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201

def get_models_with_filters(cls, filters=None):
    query = db.select(cls)

    if filters:
        for attribute, value in filters.items():
            if hasattr(cls, attribute):
                query = query.where(getattr(cls, attribute).ilike(f"%{value}%"))

    models = db.session.scalars(query.order_by(cls.id))
    models_response = [model.to_dict() for model in models]
    return models_response