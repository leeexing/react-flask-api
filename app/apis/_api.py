from flask import Blueprint
from flask_restplus import Api

api_blueprint = Blueprint('douban_api', __name__, url_prefix='/api')
api = Api(api_blueprint, prefix='/v1', title='DoubanMusicApi')
