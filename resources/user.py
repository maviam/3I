from flask_restful import Resource, reqparse
from models.user import UserModel 
from hmac import compare_digest
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from blocklist import BLOCKLIST

class User(Resource):
    #argumentos = reqparse.RequestParser()
    #argumentos.add_argument("username", type=str, required=True, help="O nome do hotel é obrigatório")
    #argumentos.add_argument("password", type=str, required=True, help="O nome do hotel é obrigatório")

    def get(self, username):
        user = UserModel.find_user(username) # Devolve o user ou None caso não encontre nenhum user
        if user is not None:
            return user.json(), 200
        return  {"mensagem": "Utilizador não foi encontrado."}

    @jwt_required()
    def delete(self, username):
        user = UserModel.find_user(username)
        if user is not None: 
            try:
                user.delete_hotel()
                return {"mensagem": "Utilizador removido com sucesso"}, 200
            except: 
                return{ "mensagem": "Um erro interno do servidor aconteceu..."}, 500 # RESPONSE ERROR 500 - erro na base de dados
        return {"mensagem": "Hotel não encontrado."}

class UserRegister(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("username", type=str, required=True, help="O username do utilizador é obrigatório")
    argumentos.add_argument("password", type=str, required=True, help="Password obrigatória")

    def post(self):
        dados = UserRegister.argumentos.parse_args()
        # Não passamos o username no URL por segurança do utlizador
        if UserModel.find_user(dados["username"]): # Verifica se ja existe algum
            return {"mensagem": "Já existe um utilizador com este username."}, 400 # Devolve uma mensagem e um RESPONSE_CODE 400
        # Se não existir já um utilizador com este username criar um novo utilizador
        novo_utilizador = UserModel(**dados)
        try:
            novo_utilizador.save_user()
            return {"mensagem": "Utilizador criado com sucesso."}, 201
        except:
            return {"mensagem": "Erro interno ocorreu..."}, 500
            
class UserLogin(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("username", type=str, required=True, help="O username do utilizador é obrigatório")
    argumentos.add_argument("password", type=str, required=True, help="Password obrigatória")

    def post(self):
        dados = UserLogin.argumentos.parse_args()
        user = UserModel.find_user(dados["username"])

        if user and compare_digest(user.password, dados["password"]):
             token = create_access_token(identity=user.username)
             return { "access_token": token}, 200
        return { "mensagem": " O utilizador ou password está incorreto"}, 401

class UserLogout(Resource):   
    @jwt_required
    def post(self):
        # Pegar o meu token e invalidar o mesmo
        jwt_id = get_jwt()["jti"] # Obter o identificador do token
        # Anexar este identificador a minha lista de token revogados
        BLOCKLIST.add(jwt_id) # Adicionar a minha lista de tokens inválidos o atual
        return { "mensagem": "Logout do utilizador efetuado com sucesso"}, 200