# Este "hotel.py" serve para os Gets, Posts...
from flask_restful import Resource, reqparse
from models.hotel import HotelModel  # importar a classe HotelModel do hotel.py em "models/"


# cada rota/endpoint(link, o get, o post...) vai ter de estar associado a uma classe
class Hoteis(Resource):
    # Buscar
    def get(self):
        # API retorna sempre um JSON(dicionário ( {"chave": "valor"} ))
        return { "hoteis": [hotel.json() for hotel in HotelModel.query.all()] }  # vai devolver cada dicionario


# API
class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("nome", type=str, required=True, help="O nome do hotel é obrigatório")
    argumentos.add_argument("estrelas", type=str, required=True, help="O nome do hotel é obrigatório")
    argumentos.add_argument("diaria", type=str, required=True, help="O nome do hotel é obrigatório")
    argumentos.add_argument("cidade", type=str, required=True, help="O nome do hotel é obrigatório")

    # Buscar
    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id) # Devolve o hotel ou None caso não encontre nenhum hotel
        if hotel is not None:
            return hotel.json(), 200
        return  {"mensagem": "Hotel não foi encontrado."}


    # Criar
    # NOTA para não achar estranho: enquanto não estamos a lidar com bases de dados os Posts não vão inserir os dados na lista para sempre, só enquanto o server estiver ligado.
    def post(self, hotel_id):  # o hotel_id vai no URL (endpoint), porque vai ser o identificador de cada hotel
        dados = Hotel.argumentos.parse_args()  # cria um dicionário com as quatro variáveis (dados)
        hotel = HotelModel.find_hotel(hotel_id)
        # verifica cada hotel se já tem um hotel_id dentro da base de dados, se existir, retorna um JSON(dicionário) com uma mensagem a avisar que o hotel já existe
        if Hotel is not None:
            return {"mensagem": f"O hotel com id {hotel_id} já existe."}  # HTTP Requests recebem e retornam sempre JSONs(que são dicionários, logo temos de retornar um dicionário)
        
        novo_hotel = HotelModel(hotel_id, **dados).json()  # dois "**" chama um dicionário

        try:  # Tenta fazer isto...
            novo_hotel.save_hotel()
            return novo_hotel, 200  # "200" é o RESPONSE CODE
        except:  # Senão...
            return{ "mensagem": "Um erro interno do servidor aconteceu..."}, 500 # RESPONSE ERROR 500 - erro na base de dados


    # Atualizar
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()  # cria um dicionário com as quatro variáveis (dados)  || "dados" é um dicionario

        # Se o hotel_id existe
        hotel = HotelModel.find_hotel(hotel_id)    
        if hotel is not None:
            try:
                hotel.update_hotel(*dados) # um asterisco "*" serve para ir buscar os valores | (se passarmos sem nenhum "*" ele devolve o dicionário todo)
                hotel.save_hotel()
                return hoteis, 200  # devolve RESPONSE CODE 201 (Created)
            except:  # Senão...
                return{ "mensagem": "Um erro interno do servidor aconteceu..."}, 500 # RESPONSE ERROR 500 - erro na base de dados
        
        # Se o hotel_id não existir, cria o hotel
        novo_hotel = HotelModel(hotel_id, **dados)  # dois "**" chama um dicionário, dois asteriscord "**" serve para is buscar as chaves/keys | (se passarmos sem nenhum "*" ele devolve o dicionário todo)
        hoteis.save_hotel()
        return novo_hotel.json(), 201  # "200" é o RESPONSE CODE


    # Apagar
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel is not None: 
            try:
                hotel.delete_hotel()
                return {"mensagem": "Hotel removido com sucesso"}, 200
            except:  # Senão...
                        return{ "mensagem": "Um erro interno do servidor aconteceu..."}, 500 # RESPONSE ERROR 500 - erro na base de dados
        return {"mensagem": "Hotel não encontrado."}

    
