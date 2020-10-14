from pathlib import Path

from flask import Flask


project_dir = Path(__file__).resolve().parent.parent
web_dir = project_dir / 'ccweb'
template_dir = project_dir / 'templates'
static_dir = project_dir / 'static'


app = Flask(
    __name__,
    template_folder=str(template_dir),
    static_folder=str(static_dir),
)

from cc.ccweb import views  # noqa: E402, F401, I100
