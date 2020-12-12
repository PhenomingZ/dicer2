from App.models import BaseModel
from App.ext import db


class JobsInfo(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    j_name = db.Column(db.String(64))
