# -*- coding: utf-8 -*-
"""Click commands."""
import os
import re
from glob import glob
from subprocess import call

import click
from flask.cli import with_appcontext

from api.extensions import db

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, "tests")
LANG_CODE_RE = re.compile(r"^[A-Za-z0-9_.@-]+$")


@click.command()
def test():
    """Run the tests."""
    import pytest

    rv = pytest.main([TEST_PATH, "--verbose"])
    exit(rv)


@click.command()
@click.option(
    "-f",
    "--fix-imports",
    default=True,
    is_flag=True,
    help="Fix imports using isort, before linting",
)
@click.option(
    "-c",
    "--check",
    default=False,
    is_flag=True,
    help="Don't make any changes to files, just confirm they are formatted correctly",
)
def lint(fix_imports, check):
    """Lint and check code style with black, flake8 and isort."""
    skip = ["node_modules", "requirements", "migrations"]
    root_files = glob("*.py")
    root_directories = [
        name for name in next(os.walk("."))[1] if not name.startswith(".")
    ]
    files_and_directories = [
        arg for arg in root_files + root_directories if arg not in skip
    ]

    def execute_tool(description, *args):
        """Execute a checking tool with its arguments."""
        command_line = list(args) + files_and_directories
        click.echo("{}: {}".format(description, " ".join(command_line)))
        rv = call(command_line)
        if rv != 0:
            exit(rv)

    isort_args = ["-rc"]
    black_args = []
    if check:
        isort_args.append("-c")
        black_args.append("--check")
    if fix_imports:
        execute_tool("Fixing import order", "isort", *isort_args)
    execute_tool("Formatting style", "black", *black_args)
    execute_tool("Checking code style", "flake8")


@click.command()
def clean():
    """Remove *.pyc and *.pyo files recursively starting at current directory.

    Borrowed from Flask-Script, converted to use Click.
    """
    for dirpath, dirnames, filenames in os.walk("."):
        for filename in filenames:
            if filename.endswith(".pyc") or filename.endswith(".pyo") or filename.endswith(".c"):
                full_pathname = os.path.join(dirpath, filename)
                click.echo("Removing {}".format(full_pathname))
                os.remove(full_pathname)


@click.command()
@with_appcontext
def db_setup():
    """create tables
    """
    db.create_all()

    try:
        db.session.execute("set global sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,"
                           "ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION'")
        db.session.commit()
    except:
        pass

    try:
        db.session.execute("set global tidb_enable_noop_functions='ON'")
        db.session.commit()
    except:
        pass


@click.group()
def translate():
    """Translation and localization commands."""


def _run_translate_command(command, err):
    if call(command):
        raise RuntimeError(err)


@translate.command()
@click.argument('lang')
def init(lang):
    """Initialize a new language."""
    if not LANG_CODE_RE.fullmatch(lang):
        raise click.BadParameter("Invalid language code", param_hint="lang")

    _run_translate_command(['pybabel', 'extract', '-F', 'babel.cfg', '-k', '_l', '-o', 'messages.pot', '.'],
                           'extract command failed')
    _run_translate_command(['pybabel', 'init', '-i', 'messages.pot', '-d', 'api/translations', '-l', lang],
                           'init command failed')
    os.remove('messages.pot')


@translate.command()
def update():
    """Update all languages."""

    _run_translate_command(['pybabel', 'extract', '-F', 'babel.cfg', '-k', '_l', '-o', 'messages.pot', '.'],
                           'extract command failed')
    _run_translate_command(['pybabel', 'update', '-i', 'messages.pot', '-d', 'api/translations'],
                           'update command failed')
    os.remove('messages.pot')


@translate.command()
def compile():
    """Compile all languages."""

    _run_translate_command(['pybabel', 'compile', '-d', 'api/translations'], 'compile command failed')
