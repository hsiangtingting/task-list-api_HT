from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from .route_utilities import validate_model, create_model, get_models_with_filters
from ..db import db

bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

@bp.get("/<task_id>")
def get_task(task_id):
    task = validate_model(Task, task_id)

    # Use Task.to_dict() to produce the expected response shape
    return task.to_dict(), 200

@bp.post("")
def create_task():
    request_body = request.get_json()

    return create_model(Task, request_body)

@bp.get("")
def get_all_tasks():
    # Build filters from query params and reuse get_models_with_filters helper
    filters = {}
    title_param = request.args.get("title")
    description_param = request.args.get("description")

    if title_param:
        filters["title"] = title_param

    if description_param:
        filters["description"] = description_param

    tasks_response = get_models_with_filters(Task, filters if filters else None)

    # Support sort query param (asc/desc) on title
    sort_order = request.args.get("sort")
    if sort_order == "asc":
        tasks_response.sort(key=lambda x: x["title"], reverse=False)
    elif sort_order == "desc":
        tasks_response.sort(key=lambda x: x["title"], reverse=True)

    return tasks_response, 200

@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]

    # Only update completed_at if provided in the request
    if "completed_at" in request_body:
        task.completed_at = request_body["completed_at"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.patch("/<task_id>/mark_complete")
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = db.func.now()
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.patch("/<task_id>/mark_incomplete")
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None
    db.session.commit()

    return Response(status=204, mimetype="application/json")


# def validate_task(task_id):
#     try:
#         task_id = int(task_id)
#     except:
#         response = {"message":f"task {task_id} invalid"}
#         abort(make_response(response, 400))

#     task = db.session.get(Task, task_id)
#     if task:
#         return task

#     response = {"message": f"task {task_id} not found"}
#     abort(make_response(response, 404))
