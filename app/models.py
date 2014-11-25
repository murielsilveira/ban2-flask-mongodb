import datetime
from flask import url_for
from app import db


class Filme(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    titulo = db.StringField(verbose_name="Titulo", max_length=50, required=True)
    diretor = db.StringField(verbose_name="Diretor", max_length=50, required=True)    
    categoria = db.StringField(verbose_name="Categoria", max_length=50, required=True)
    descricao = db.StringField(verbose_name="Descricao", max_length=200, required=False)

    def __unicode__(self):
        return self.titulo

    meta = {
        'indexes': ['titulo', 'diretor', 'categoria'],
        'ordering': ['titulo']
    }
