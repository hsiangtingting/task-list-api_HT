from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from app.models.goal import Goal
from .route_utilities import validate_model, create_model, get_models_with_filters
from ..db import db

bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_task():
    request_body = request.get_json()

    return create_model(Goal, request_body)

@bp.get("/<goal_id>")
def get_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    # Use Goal.to_dict() to produce the expected response shape
    return goal.to_dict(), 200

@bp.get("")
def get_all_goals():
    # Build filters from query params and reuse get_models_with_filters helper
    filters = {}
    title_param = request.args.get("title")

    if title_param:
        filters["title"] = title_param

    goals_response = get_models_with_filters(Goal, filters if filters else None)

    # Support sort query param (asc/desc) on title
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

# @bp.patch("/<goal_id>/mark_complete")
# def mark_goal_complete(goal_id):
#     goal = validate_model(Goal, goal_id)

#     goal.completed_at = db.func.now()
#     db.session.commit()

#     return Response(status=204, mimetype="application/json")

# @bp.patch("/<goal_id>/mark_incomplete")
# def mark_goal_incomplete(goal_id):
#     goal = validate_model(Goal, goal_id)

#     goal.completed_at = None
#     db.session.commit()

#     return Response(status=204, mimetype="application/json")