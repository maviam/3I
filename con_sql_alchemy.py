# Ele olha para uma classe e transforma tudo em código sql e manda para a base de dados
# Temos de ativar o sql_alchemy pelo terminal:
#
# python -m pip install Flask-SQLAlchemy

from flask_sqlalchemy import SQLAlchemy

bd = SQLAlchemy() # Base de dados da API gerida pelo SQLAlchemy, que é uma biblioteca que vai criar a base de dados e gerir a mesma
