from flask import Blueprint

collect_bp = Blueprint(
    "collect_bp",
    __name__,
    url_prefix="/collect",
)
from .views import *
