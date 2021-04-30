from flask_restful import Api

from resources.user import UserRegister, UserLogin, User, TokenRefresh, UserLogout, ConfirmToken, Confirm, Reset, ResetPassword, Follow, Unfollow
from resources.item import Item, ItemList
from resources.store import Store, StoreList

api = Api()

api.add_resource(Unfollow, "/unfollow/<int:user_id>")
api.add_resource(Follow, "/follow/<int:user_id>")
api.add_resource(Confirm, "/confirm")
api.add_resource(ConfirmToken, "/confirm/<string:token>", endpoint="confirmtoken")
api.add_resource(Reset, "/reset")
api.add_resource(ResetPassword, "/resetpassword/<string:token>", endpoint="resetpassword")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")
