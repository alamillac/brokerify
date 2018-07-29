from flask import current_app
from flask import request
from flask_restful import Resource
from web.api.security import requires_auth
from modules.logger import context
from app.models.core import User, PortfolioStock, PortfolioDividend, db_session
from web.api.serializer import UserSchema, PortfolioStockSchema, PortfolioDividendSchema
from web.api.forms import UserStockForm
from marshmallow import ValidationError


user_schema = UserSchema()
users_schema = UserSchema(many=True)
portfolio_stock_schema = PortfolioStockSchema(many=True)


class UserResource(Resource):
    @requires_auth
    def get(self, username=None):
        context.update_uuid()
        if username:
            current_app.logger.debug("Showing user %s", id)
            user = User.get(username)
            response = user_schema.dump(user)
            return response.data, 200

        current_app.logger.debug("Showing all users")
        users = User.all()
        response = users_schema.dump(users)
        return response.data, 200


class UserStockResource(Resource):
    @requires_auth
    def get(self, portfolio_id, transaction_id=None):
        context.update_uuid()
        if not transaction_id:
            stock_transactions = PortfolioStock.get_list(portfolio_id)
            response = portfolio_stock_schema.dump(stock_transactions)
            return response.data, 200

        stock_transaction = PortfolioStock.get(transaction_id)
        if not stock_transaction or stock_transaction.portfolio_id != portfolio_id:
            return [], 404
        response = PortfolioStockSchema().dump(stock_transaction)
        return response.data, 200

    @requires_auth
    def post(self, portfolio_id, transaction_id=None):
        context.update_uuid()
        data = request.get_json()
        if not data:
            return {"error": "Invalid data"}, 400

        data["portfolio_id"] = portfolio_id
        result = UserStockForm().load(data)
        if result.errors:
            return {"error": "Invalid data", "fields": result.errors}, 400

        stock_transaction = PortfolioStock.add(result.data)
        response = PortfolioStockSchema().dump(stock_transaction)
        return response.data, 201

    @requires_auth
    def put(self, portfolio_id, transaction_id):
        context.update_uuid()
        data = request.get_json()
        if not data:
            return {"error": "Invalid data"}, 400

        data.update({
            "portfolio_id": portfolio_id,
            "id": transaction_id
        })
        result = UserStockForm().load(data)
        if result.errors:
            return {"error": "Invalid data", "fields": result.errors}, 400

        stock_transaction = PortfolioStock.get(transaction_id)
        if not stock_transaction or stock_transaction.portfolio_id != portfolio_id:
            return [], 404

        stock_transaction = PortfolioStock.update(transaction_id, result.data)
        response = PortfolioStockSchema().dump(stock_transaction)
        return response.data, 200

    @requires_auth
    def delete(self, portfolio_id, transaction_id):
        context.update_uuid()
        stock_transaction = PortfolioStock.get(transaction_id)
        if not stock_transaction or stock_transaction.portfolio_id != portfolio_id:
            return [], 404

        response = PortfolioStockSchema().dump(stock_transaction)
        db_session.delete(stock_transaction)
        return response.data, 200


class UserDividendResource(Resource):
    @requires_auth
    def get(self, portfolio_id, dividend_id=None):
        context.update_uuid()
        if not dividend_id:
            stock_dividend = PortfolioDividend.get_list(portfolio_id)
            response = PortfolioDividendSchema(many=True).dump(stock_dividend)
            return response.data, 200

        stock_dividend = PortfolioDividend.get(dividend_id)
        if not stock_dividend or stock_dividend.portfolio_id != portfolio_id:
            return [], 404
        response = PortfolioDividendSchema().dump(stock_dividend)
        return response.data, 200

