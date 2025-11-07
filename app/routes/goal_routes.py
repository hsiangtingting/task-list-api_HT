from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from app.models.goal import Goal
from .route_utilities import validate_model, create_model, get_models_with_filters, get_models_or_abort
from ..db import db

bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()

    return create_model(Goal, request_body)

@bp.get("/<goal_id>")
def get_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return goal.to_dict(), 200

@bp.get("")
def get_all_goals():
    filters = {}
    title_param = request.args.get("title")

    if title_param:
        filters["title"] = title_param

    goals = db.session.query(Goal).filter_by(**filters).all()
    goals_response = [goal.to_dict() for goal in goals]

    sort_order = request.args.get("sort")
    if sort_order == "asc":
        goals_response.sort(key=lambda x: x["title"], reverse=False)
    elif sort_order == "desc":
        goals_response.sort(key=lambda x: x["title"], reverse=True)

    return goals_response, 200

@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.post("/<goal_id>/tasks")
def link_task_id_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    task_ids_to_link = request_body.get("task_ids")

    if not task_ids_to_link or not isinstance(task_ids_to_link, list):
        abort(400, description="Request body must contain a list of 'task_ids'.")

    for task in goal.tasks:
        task.goal_id = None

    tasks_to_update = get_models_or_abort(Task, task_ids_to_link)

    for task in tasks_to_update:
        task.goal_id = goal.id

    db.session.commit()

    response_body = {
        "id": goal.id,
        "task_ids": [task.id for task in tasks_to_update]
    }

    return response_body, 200

@bp.get("/<goal_id>/tasks")
def get_tasks_content_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks_response = [task.to_dict() for task in goal.tasks]

    response_body = {
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks_response
    }
    return response_body, 200

