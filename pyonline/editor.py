import functools
import subprocess
import ast
import re
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('editor', __name__, url_prefix='/editor')


@bp.route("/")
def editor():
    return render_template("editor.html")


def is_code_secure(code):

    word_list = ["import sys", "import os", "exec", "import socket", "import subprocess", "import shutil",
                 "import urllib.request",
                 "with open", "import pickle"]

    pattern = "|".join(word_list)

    if re.search(pattern, code):
        return 0
    return 1


@bp.route("/run_code", methods=["GET", "POST"])
def run_code():
    code = request.form['code']
    code_input = request.form["input"].strip("\"").replace("\\n", "\n")
    code = re.sub(r'input\([^)]*\)', 'input()', code)

    if not is_code_secure(code):
        return ("\nYou are not allowed to execute this code.\n" + ("This might be because it contains "
                                                                 "sensitive/malicious code or libraires.\n") +
                "\nExample : Things like os and sys module are not allowed to execute.")

    try:
        result = subprocess.check_output(['python', '-c', code], input=code_input, stderr=subprocess.STDOUT, text=True)
        print(result)
        return result
    except subprocess.CalledProcessError as e:
        return e.output
