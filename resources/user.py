# Este "hotel.py" serve para os Gets, Posts...
from flask_restful import Resource, reqparse
from models.user import UserModel  # importar a classe HotelModel do hotel.py em "models/"
from hmac import compare_digest

# cada rota/endpoint(link, o get, o post...) vai ter de estar associado a uma classe
# API
class User(Resource):
    #argumentos = reqparse.RequestParser()
    #argumentos.add_argument("username", type=str, required=True, help="O nome do hotel é obrigatório")
    #argumentos.add_argument("password", type=str, required=True, help="O nome do hotel é obrigatório")


    # Buscar
    def get(self, username):
        user = UserModel.find_user(username) # Devolve o user ou None caso não encontre nenhum user
        if user is not None:
            return user.json(), 200
        return  {"mensagem": "Utilizador não foi encontrado."}


    # Apagar
    def delete(self, username):
        user = UserModel.find_user(username)
        if user is not None: 
            try: # Tenta fazer isto...
                user.delete_hotel()
                return {"mensagem": "Utilizador removido com sucesso"}, 200
            except: # Se der errado...
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
        ...