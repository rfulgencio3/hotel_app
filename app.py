from flask import Flask, jsonify
from flask_restful import Api
from blacklist import BLOCKLIST
from resources.hotel import Hoteis, Hotel
from resources.usuario import Usuario, UsuarioRegistro, UsuarioLogin, UsuarioLogout
from resources.site import Site, Sites
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def cria_banco():
    banco.create_all()
    
@jwt.token_in_blocklist_loader
def verifica_blocklist(self, token):
    return token['jti'] in BLOCKLIST

@jwt.revoked_token_loader
def token_invalidado(jwt_header, jwt_payload):
    return jsonify({'message': 'ALERADY_LOGGED_OUT_BLOCKED_TOKEN'}), 401

api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(Usuario, '/usuarios/<int:user_id>')
api.add_resource(UsuarioRegistro, '/cadastro')
api.add_resource(UsuarioLogin, '/login')
api.add_resource(UsuarioLogout, '/logout')
api.add_resource(Sites, '/sites')
api.add_resource(Site, '/sites/<string:url>')

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
