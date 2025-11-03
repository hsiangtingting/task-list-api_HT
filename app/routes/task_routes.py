from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from ..db import db

tasks_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")


def get_task_or_abort(task_id):
    task = db.session.get(Task, task_id)

    if task is None:
        abort(404, description=f"Task{task_id} not found")

    return task

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        response = {"message":f"task {task_id} invalid"}
        abort(make_response(response, 400))

    task = db.session.get(Task, task_id)
    if task:
        return task

    response = {"message": f"task {task_id} not found"}
    abort(make_response(response, 404))

@tasks_bp.get("/<task_id>")
def get_task(task_id):
    task = validate_task(task_id)

    response = dict(
        id=task.id,
        title=task.title,
        description=task.description,
        completed_at=task.completed_at
    )

    return response

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()
    title = request_body["title"]
    description = request_body["description"]
    completed_at = request_body["completed_at"]

    new_task = Task(title=title, description=description, completed_at=completed_at)
    db.session.add(new_task)
    db.session.commit()

    response = dict(
        id=new_task.id,
        title=new_task.title,
        description=new_task.description,
        completed_at=new_task.completed_at
    )

    if not completed_at:
        response["is_complete"] = False
    else:
        response["is_complete"] = True

    if not response :
        return {"details": "Invalid data"}, 400

    return response, 201

@tasks_bp.get("")
def get_all_tasks():
    query = db.select(Task)
    title_param = request.args.get("title")
    description_param = request.args.get("description")

    if title_param:
        query = query.where(Task.title == title_param)

    if description_param:
        query = query.where (task.description.ilike(f"%{description_param}%"))

    tasks = db.session.scalars(query.order_by(Task.id))
    # query = query.order_by(Task.id)
    # tasks = db.session.scalars(query)

    tasks_response = []
    for task in tasks:
        tasks_response.append(dict(
            id=task.id,
            title=task.title,
            description=task.description,
            completed_at=task.completed_at
        ))

    return tasks_response, 200

@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body["completed_at"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@tasks_bp.delete("/<book_id>")
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        response = {"message":f"task {task_id} invalid"}
        abort(make_response(response, 400))

    task = db.session.get(Task, task_id)
    if task:
        return task

    response = {"message": f"task {task_id} not found"}
    abort(make_response(response, 404))

