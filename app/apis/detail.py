from flask_restplus import Resource, Namespace

ns = Namespace('detail', description='豆瓣音乐--详情')

@ns.route('')
class Detail(Resource):
    def get(self):
        return {'message': 'Welcome to douban music api'}
