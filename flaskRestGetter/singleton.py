from app import db
from models import Operador, MementoNotificacao

class Caretaker:

    SingleInstance = None

    @staticmethod
    def getInstance():
        if(Caretaker.SingleInstance is None):
            Caretaker.SingleInstance = Caretaker()
        return Caretaker.SingleInstance

    def createMemento(self, maquina):
        memento = maquina.new_memento()
        db.session.add(memento)
        db.session.commit()
        return memento

    def getAllMementos(self, id):
        operador = Operador.query.get(id)
        notificacoes = MementoNotificacao.query.filter(MementoNotificacao.idMaquina.in_([maquina.id for maquina in operador.maquinas])).all()
        
        return notificacoes
    