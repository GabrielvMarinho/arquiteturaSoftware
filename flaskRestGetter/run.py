from app import create_app, db
import threading
from random import randint
from flask_socketio import SocketIO
from time import sleep
from models import Maquina, Operador
from singleton import Caretaker
import math
import requests

app, socketio = create_app()

def tarefa():
    while True:
        with app.app_context():

            operadores = Operador.query.all()
            maquinas = Maquina.query.all()

            for maquina in maquinas:
                for (cDados, vDados), (msgMax, dadoMax),(msgMin, dadoMin), tipoMensagemMax, tipoMensagemMin in zip(maquina.dadosDict.items(), maquina.maxDict.items(), maquina.minDict.items(), maquina.tipoMensagemMax, maquina.tipoMensagemMin):
                    # teste para mandar notificação plo observer:

                    url = "http://127.0.0.1:8081/iotDataGet" 
                    response = requests.get(url)
                    content = response.content.decode('utf-8')  # Decode the bytes to string
                    dado = float(content)

                    # distancia = math.sqrt((dadoMin - dadoMax) ** 2)
                    # dado = randint(int(dadoMin-distancia*0.01), int(dadoMax+distancia*0.01))
                    
                    #mudando o valor dos dados da máquina em si
                    maquina.dadosDict[cDados] = dado

                    if dado>dadoMax:
                        #criar uma notificação para cada operador
                        operadores = Operador.query.all()
                        for operador in operadores:

                            #checando se o operador possui aquela máquina no conjunto de máquinas
                            if any(maquinax.id == maquina.id for maquinax in operador.maquinas):

                                
                                notificacaoDict = {
                                    "mensagem":maquina.nome,
                                    "mensagem1":msgMax,
                                    "mensagem2":"status | "+cDados+": "+str(dado),
                                    "tipoMensagem": tipoMensagemMax,
                                    "idMaquina": maquina.id,
                                    "idOperador": operador.id    
                                }
                                
                                socketio.emit('notificacoes',notificacaoDict, room=operador.id)
                                #caretaker chamando seu metodos estatico para criar um memento
                                Caretaker.getInstance().createMemento(maquina)
                    
                    elif dado<dadoMin:

                        #criar uma notificação para cada operador
                        for operador in operadores:
                            #checando se o operador possui aquela máquina no conjunto de máquinas
                            if any(maquinax.id == maquina.id for maquinax in operador.maquinas):
                                notificacaoDict = {
                                    "mensagem": maquina.nome,
                                    "mensagem1":msgMin,
                                    "mensagem2":"status | "+cDados+": "+str(dado),
                                    "tipoMensagem": tipoMensagemMin,
                                    "idMaquina": maquina.id,
                                    "idOperador": operador.id    
                                }
                                
                                socketio.emit('notificacoes',notificacaoDict, room=operador.id)
                                #caretaker chamando seu metodos estatico para criar um memento

                                Caretaker.getInstance().createMemento(maquina)
                    

                db.session.commit()
            
            for operador in operadores:
                dados = {}
                
                for maquina in operador.maquinas:
                    dados[maquina.id] = list(maquina.dadosDict.values())     

                socketio.emit('atualizar_dados',dados, room=operador.id)

        sleep(2)





if __name__ == "__main__":
    thread = threading.Thread(target=tarefa)
    thread.start()
    socketio.run(app)

