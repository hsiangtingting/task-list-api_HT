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

