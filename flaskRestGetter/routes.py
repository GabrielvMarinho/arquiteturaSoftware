from flask import render_template, request, redirect, url_for, jsonify, json, flash, request
from models import Operador, Maquina
from forms import SignUpForm, dadosMaquina, cadastroMaquina
from flask_login import current_user, logout_user, login_user, login_required
from flask_socketio import join_room
from singleton import Caretaker

print("dasdasdasd")
def register_routes(app, db, socketio):

    @socketio.on("user_join")
    def conectar_operador(id):
        join_room(id)
        print("Operador conectado á sala "+str(id))
        
    

    @app.route("/historico")
    def retornar_historico():
        notificacoes = Caretaker.getInstance().getAllMementos(current_user.id)
        return render_template("historico.html", notificacoes=notificacoes)

    @app.route("/retornar_user")
    def retornar_user():
        return current_user
    
    #routes relacionado aos atributos -----------------------------------------------------
    @app.route("/lista_maquinas_atributos")
    @login_required
    def lista_maquinas_atributos():
        maquinas = Maquina.query.all()
        return render_template("lista_maquinas_atributos.html", maquinas=maquinas)

    #adicionar atributo
    @app.route("/adicionando_atributos/<id>", methods=["POST", "GET"])
    @login_required
    def add_atributo(id):
        form = dadosMaquina()
        maquina = Maquina.query.get(id)
        if form.validate_on_submit():
        
            if any(i == form.nomedado.data for i in maquina.dadosDict):
                flash("Já existe esse ATRIBUTO nesta máquina")
                return redirect(url_for("add_atributo", id=id))
            elif any(i == form.msgErroMax.data for i in maquina.maxDict):
                flash("Já existe esta MENSAGEM DE ERRO MÁXIMO nesta máquina")
                return redirect(url_for("add_atributo", id=id))
            elif any(i == form.msgErroMin.data for i in maquina.minDict):
                flash("Já existe esta MENSAGEM DE ERRO MÍNIMO nesta máquina")
                return redirect(url_for("add_atributo", id=id))

            else:
                maquina.dadosDict[form.nomedado.data] = 100
                maquina.minDict[form.msgErroMin.data] = form.minMaquina.data
                maquina.maxDict[form.msgErroMax.data] = form.maxMaquina.data

                maquina.tipoMensagemMax.append(form.optionMax.data)
                maquina.tipoMensagemMin.append(form.optionMin.data)
                
                db.session.commit()
                return redirect(url_for("painel_controle"))
                
        return render_template('adicionar_atributo.html', form=form)  
    #------------------------------------------------------------------------

    @app.route("/retornar_dados")
    @login_required
    def retornar_dados():
        dados =[]
        maquinas = current_user.maquinas
        for i in maquinas:
            dados.append(i.nome)
            dados.append(i.dadosDict)
        return jsonify(dados)


    
    #mostra a lista de máquinas para adicionar a relação
    @app.route("/adicionar_relação", methods=["GET", "POST"])
    @login_required
    def add_relacao():
        maquinas = Maquina.query.all()
        maquinasrel= current_user.maquinas
        return render_template("mudar_relacao.html", maquinas = maquinas, maquinasrel=maquinasrel)
    #adiciona a relação de fato
    @app.route("/add_rel<id>", methods=["GET", "POST"])
    @login_required
    def add_rel(id):
        
        maquina = Maquina.query.filter_by(id = id).first()
        maquinas = Maquina.query.all()

        if maquina in current_user.maquinas:
            print("entrou")
            current_user.maquinas.remove(maquina)
            db.session.commit()
            return render_template("mudar_relacao.html", maquinas =maquinas)

        current_user.maquinas.append(maquina)# cria a relação de maquina e usuário
        db.session.commit()
        return render_template("mudar_relacao.html", maquinas =maquinas)

    #adicionar maquinas no servidor
    @app.route("/adicionar_maquinas", methods=["GET", "POST"])
    @login_required
    def adicionar_maquinas():
        form = cadastroMaquina()
        if form.validate_on_submit():
            maquina = Maquina.query.filter_by(nome=form.nome.data).first()
            if maquina:
                flash("Máquina com nome JÁ EXISTENTE!")
                return redirect(url_for("adicionar_maquinas"))
            maquina = Maquina(
                nome = form.nome.data,
                dadosDict = {},
                maxDict = {},
                minDict = {}
            )
            db.session.add(maquina)
            db.session.commit()
            return redirect(url_for("painel_controle"))
        return render_template("adicionar_maquinas.html", form=form)
    
    @app.route("/minhas_maquinas")
    @login_required
    def minhas_maquinas():
        maquinas = current_user.maquinas
        return render_template("minhas_maquinas.html", maquinas=maquinas)
    
    
    
    @app.route("/painel_controle")
    @login_required
    def painel_controle():
        maquinas = current_user.maquinas
        listaMaquinas = [{"id":maquina.id, "nome":maquina.nome, "dados":list(maquina.dadosDict.keys())} for maquina in maquinas]
        return render_template("painel_controle.html", maquinas = listaMaquinas)
    
    #routes relacionado ao login-----------------------------------------------------
    @app.route("/sair")
    @login_required
    def sair():
        logout_user()
        return redirect(url_for("login"))
    
    @app.route('/signup', methods=["GET", "POST"])
    def signup():
        form = SignUpForm()
        if form.validate_on_submit():
            operadores = Operador.query.all()
            
            operador = Operador(
                username = form.username.data,
                password = form.password.data,
            )
            
            db.session.add(operador)
            db.session.commit()
            return redirect(url_for("login"))
        return render_template('signup.html', form=form)

    @app.route('/', methods=["GET", "POST"])
    def login():
        form = SignUpForm()
        if form.validate_on_submit():
            nome = form.username.data
            operador = Operador.query.filter_by(username = nome).first()
            if operador:
                if operador.password == form.password.data:
                    login_user(operador)
                    return redirect(url_for("painel_controle"))
                else:
                    flash("Senha INCORRETA!")
                    return redirect(url_for("login"))
            else:
                flash("Usuário NÃO EXISTE!")
                return redirect(url_for("login"))
        return render_template('login.html', form=form)
    #------------------------------------------------------------------------

    
    
    
