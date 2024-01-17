import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('welcome', __name__)


@bp.route("/")
def welcome():
    return render_template("welcome.html")
