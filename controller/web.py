import datetime as dt
from db import customers, generate_new_id
from flask import Blueprint, redirect, render_template, request, flash


web = Blueprint('Web', __name__)


@web.route('/', methods=["GET"])
def index():
    data = [customer.copy() for customer in customers]
    params = dict(request.args)
    
    if params.get('q') is not None and params.get('q') != '':
        data = list(filter(lambda customer: 
            params.get('q') in customer.get('nome') 
            or customer.get('cpf').startswith(params.get('q')), data))

    return render_template('index.html', data=customers)

@web.route('/create', methods=["GET"])
def create():
    return render_template('create.html')

@web.route('/create', methods=["POST"])
def save():
    erro = False
    data = dict(request.form)
    
    if data.get("name") is None or data.get("name").strip() == '':
        flash('O campo nome é obrigatório.')
        erro = True
    
    if data.get('cpf') is None or data.get('cpf').strip() == '':
        flash('O campo cpf é obrigatório.')
        erro = True
    
    if len(data.get('cpf')) != 11:
        flash('O campo cpf deve conter 11 digítos.')
        erro = True
    
    try:
        birth_date = dt.datetime.strptime(data.get('birth_date'), '%Y-%m-%d')
        print(birth_date)
    except Exception as err:
        flash('O campo data de nascimento está inválido.')
        erro = True

    if erro is True:
        return redirect('/create')

    new_customer = {
        "id": generate_new_id(),
        "nome": data.get('name'),
        "cpf": data.get('cpf'),
        "data_nascimento": birth_date.date()
    }
    customers.append(new_customer)
    return redirect('/')

@web.route('/edit/<int:id>', methods=["GET"])
def edit(id: int):
    for customer in customers:
        if customer.get('id') == id:
            return render_template('edit.html', customer=customer)
        
    return render_template('not_found.html') 

@web.route('/edit/<int:id>', methods=["POST"])
def update(id: int):
    current_customer = None

    for customer in customers:
        if customer.get('id') == id:
            current_customer = customer
    
    if current_customer is None:
        return render_template('not_found.html') 

    erro = False
    data = dict(request.form)
    
    if data.get("name") is None or data.get("name").strip() == '':
        flash('O campo nome é obrigatório.')
        erro = True
    
    if data.get('cpf') is None or data.get('cpf').strip() == '':
        flash('O campo cpf é obrigatório.')
        erro = True
    
    if len(data.get('cpf')) != 11:
        flash('O campo cpf deve conter 11 digítos.')
        erro = True
    
    try:
        birth_date = dt.datetime.strptime(data.get('birth_date'), '%Y-%m-%d')
        print(birth_date)
    except Exception as err:
        flash('O campo data de nascimento está inválido.')
        erro = True

    if erro is True:
        return redirect(f'/edit/{id}')

    current_customer.update({
        "nome": data.get('name'),
        "cpf": data.get('cpf'),
        "data_nascimento": birth_date.date()
    })
    return redirect('/')

@web.route('/delete/<int:id>', methods=["GET"])
def delete(id: int):
    for idx, customer in enumerate(customers):
        if customer.get('id') == id:
            customers.pop(idx)
            return redirect('/')

    return render_template('not_found.html')