from flask_restful import Api
from web.api.views.user import UserResource, UserStockResource, UserDividendResource

def init_app(app):
    api = Api(app)
    api.add_resource(UserResource, '/api/user', '/api/user/<string:username>')
    api.add_resource(UserStockResource, '/api/portfolio/<int:portfolio_id>/transaction', '/api/portfolio/<int:portfolio_id>/transaction/<int:transaction_id>')
    api.add_resource(UserDividendResource, '/api/portfolio/<int:portfolio_id>/dividend', '/api/portfolio/<int:portfolio_id>/dividend/<int:dividend_id>')
