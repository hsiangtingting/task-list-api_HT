from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from ..db import db
from .route_utilities import validate_model

bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

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

@bp.get("/<task_id>")
def get_task(task_id):
    task = validate_model(Task, task_id)

    # Use Task.to_dict() to produce the expected response shape
    return task.to_dict(), 200

@bp.post("")
def create_task():
    request_body = request.get_json()
    # title = request_body["title"]
    # description = request_body["description"]
    # completed_at = request_body["completed_at"]

    # Validate required fields
    if not request_body or "title" not in request_body or "description" not in request_body:
        return {"details": "Invalid data"}, 400

    new_task = Task.from_dict(request_body)
    db.session.add(new_task)
    db.session.commit()

    # new_task = dict(
    #     id=new_task.id,
    #     title=new_task.title,
    #     description=new_task.description,
    #     completed_at=new_task.completed_at
    # )

    # try:
    #     title = request_body["title"]
    #     description = request_body["description"]
    #     completed_at = request_body["completed_at"]
    #     new_task = Task(title=title, description=description, completed_at=completed_at)

    # except KeyError as error:
    #     response = {"message": f"Invalid request: missing {error.args[0]}"}
    #     abort(make_response(response, 400))


    # if not completed_at:
    #     response["is_complete"] = False
    # else:
    #     response["is_complete"] = True

    # if not new_task :
    #     return {"details": "Invalid data"}, 400

    return new_task.to_dict(), 201

@bp.get("")
def get_all_tasks():
    query = db.select(Task)
    title_param = request.args.get("title")
    description_param = request.args.get("description")

    if title_param:
        query = query.where(Task.title == title_param)

    if description_param:
        query = query.where (Task.description.ilike(f"%{description_param}%"))

    tasks = db.session.scalars(query.order_by(Task.id))
    # query = query.order_by(Task.id)
    # tasks = db.session.scalars(query)

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())

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



