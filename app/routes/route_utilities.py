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

def get_models_or_abort(Model, id_list):
    """
    Fetches a list of model instances by ID.
    Aborts with 404 if any ID in the list does not exist.
    """
    # 1. Query the database for all instances matching the list of IDs
    instances = db.session.query(Model).filter(Model.id.in_(id_list)).all()

    # 2. Check if the number of fetched instances matches the number of IDs requested
    if len(instances) != len(id_list):
        # Determine exactly which IDs were missing
        found_ids = {instance.id for instance in instances}
        missing_ids = [tid for tid in id_list if tid not in found_ids]

        # 3. Abort the request if any IDs are missing
        if missing_ids:
            # Note: Customize the description to fit your exact test/requirement,
            # but 404 is the correct response for a missing resource.
            abort(404, description=f"{Model.__name__}(s) with ID(s) {missing_ids} not found.")

    return instances