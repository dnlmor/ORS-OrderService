from flask import Blueprint
from flask_graphql import GraphQLView
from .schema import schema

order_blueprint = Blueprint('order', __name__)

order_blueprint.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)
