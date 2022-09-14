from flask_restful import Resource, reqparse
from blacklist import BLOCKLIST
from models.usuario import UsuarioModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="LOGIN_CANNOT_BE_NULL")
atributos.add_argument('senha', type=str, required=True, help="PASSWORD_CANNOT_BE_NULL")

class Usuario(Resource):
   # /usuarios/{user_id}
    def get(self, user_id):
        usuario = UsuarioModel.find_user(user_id)
        if usuario:
            return usuario.json()
        return {"message": "USUARIO_NOT_FOUND"}, 404

    @jwt_required()
    def delete(self, user_id):
        user = UsuarioModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {"message": "INTERNAL_ERROR_TRYING_TO_DELETE_USER"}, 500
            return {'message': 'USER_%s_DELETED' %(user.user_id)}, 200
        return {"message": "USER_NOT_FOUND"}, 404

class UsuarioRegistro(Resource):
    # /cadastro
    def post(self):
        dados = atributos.parse_args()
        
        if UsuarioModel.find_by_login(dados['login']):
            return {'message': 'LOGIN_%s_ALREADY_EXISTS' %(dados['login'].upper())}, 409

        user = UsuarioModel(**dados)
        user.save_user()
        return {'message': 'USER_%s_CREATED' %(dados['login'].upper())}, 201
    
class UsuarioLogin(Resource):
    # /login
    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        user = UsuarioModel.find_by_login(dados.login)
        if user and user.senha == dados['senha']:
            token_acesso = create_access_token(identity=user.user_id)
            return {'access_token': token_acesso}, 200
        return {'message': 'INCORRECT_USER_OR_PASSWORD'}, 401

class UsuarioLogout(Resource):
    # /logout
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] #JWT Token Identifier
        BLOCKLIST.add(jwt_id)
        return {'message': "SUCCESS_LOGOUT"}, 200
        
    