from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from app.models.goal import Goal
from .route_utilities import validate_model, create_model
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

@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    goal.title = request_body["title"]
    goal.description = request_body["description"]

    # Only update completed_at if provided in the request
    if "completed_at" in request_body:
        goal.completed_at = request_body["completed_at"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.patch("/<goal_id>/mark_complete")
def mark_goal_complete(goal_id):
    goal = validate_model(Goal, goal_id)

    goal.completed_at = db.func.now()
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.patch("/<goal_id>/mark_incomplete")
def mark_goal_incomplete(goal_id):
    goal = validate_model(Goal, goal_id)

    goal.completed_at = None
    db.session.commit()

    return Response(status=204, mimetype="application/json")