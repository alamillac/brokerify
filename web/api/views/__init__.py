from flask_restful import Api
from web.api.views.security import Login
from web.api.views.user import UserResource, UserStockResource, UserDividendResource
from web.api.views.index import IndexResource
from web.api.views.stock import StockResource

def init_app(app):
    api = Api(app)
    api.add_resource(Login, '/login')

    # User resources
    api.add_resource(UserResource, '/api/user', '/api/user/<string:username>')
    api.add_resource(UserStockResource, '/api/portfolio/<int:portfolio_id>/transaction', '/api/portfolio/<int:portfolio_id>/transaction/<int:transaction_id>')
    api.add_resource(UserDividendResource, '/api/portfolio/<int:portfolio_id>/dividend', '/api/portfolio/<int:portfolio_id>/dividend/<int:dividend_id>')

    # Index resources
    api.add_resource(IndexResource, '/api/index', '/api/index/<string:index_id>')

    # Stock resources
    api.add_resource(StockResource, '/api/stock', '/api/stock/<string:stock_id>')
