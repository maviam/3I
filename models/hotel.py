# Este contrutor vai servir para qunado eu quiser criar uma class sem adicionar a base de dados
from con_sql_alchemy import bd

class HotelModel(bd.Model):
    __tablename__ = "hoteis"  # nome da tabela que vai ser criada na base de dados
    hotel_id = bd.Column(bd.String, primary_key=True)
    nome = bd.Column(bd.String(80))
    estrelas = bd.Column(bd.Float(precision=1))
    diaria = bd.Column(bd.Float(precision=2))
    cidade = bd.Column(bd.String(80))

    # Construtor
    def __init__(self,hotel_id,nome,estrelas,diaria,cidade):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    # Quando quisermos transformar em json é so fazer por exemplo: "x = x.json"
    def json(self):
        return {"hotel_id": self.hotel_id, "nome": self.nome, "estrelas": self.estrelas, "diaria": self.diaria, "cidade": self.cidade}

    @classmethod  # Decorador  || diz que é um método da classe, porque não esta associado a um hotel em especifico (neste caso ele vai procurar um hotel qualquer)
    def find_hotel(cls, hotel_id):
        hotel = cls.query.filter_by(hotel_id = hotel_id).first() # hotel_id da tabela da base de dados = hotel_id deste método  || first() retorna uma lista dos hoteis, que neste caso vai ser só 1
        # no SQL seria: SELECT * FROM hoteis WHERE hotel_id = hotel_id LIMIT 1
        # lembrando que o SQLAlchemy transforma o codigo em SQL e executa na base de dados direta
        if hotel:
            return hotel
        return None


    def save_hotel(self):
        bd.session.add(self)
        bd.session.commit()  # commit para a base de dados para enviar os dados
        # Problema deste código: numa base de dados normal os dados sao enviados todos ou não são enviados, este codigo coloca dados um por um de cada vez nas tabelas,
        # logo se a luz for abaixo ele pode colocar alguns dos dados enviamos e outros não oque está mal, ele devia colocar os dados todos ou nenhuns

    
    def update_hotel(self, nome_atualizado, estrelas_atualizadas, diaria_atualizada, cidade_atualizada):
        self.nome = nome_atualizado
        self.estrelas = estrelas_atualizadas
        self.diaria = diaria_atualizada
        self.cidade = cidade_atualizada

    
    def delete_hotel(self):
        bd.session.delete(self)  # Delete próprio do python
        bd.session.commit()

        