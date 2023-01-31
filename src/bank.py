from flask import Blueprint

bank = Blueprint(
    "bank",
    __name__,
    url_prefix="/api/bank"
    )

@bank.get('/')
def get_all():
    return {"banks":[]}
