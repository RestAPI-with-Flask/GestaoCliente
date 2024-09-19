import datetime as dt
from http import HTTPStatus
from db import customers, generate_new_id
from flask import Blueprint, request


api = Blueprint('Api', __name__)


@api.route('/api/customers', methods=["GET"])
def get_all_customers():
    data = [customer.copy() for customer in customers]
    
    if len(data) == 0:
        return ('', HTTPStatus.NO_CONTENT)

    for customer in data:
        birth_date: dt.date = customer.get('data_nascimento')
        customer.update({
            'data_nascimento': birth_date.strftime('%Y-%m-%d')
        })

    return data

@api.route('/api/customers/<int:id>', methods=["GET"])
def detail_customer(id: int):
    for customer in customers:
        if customer.get('id') == id:
            return customer

    return (
        { 'message': 'Cliente não encontrado' }, 
        HTTPStatus.NOT_FOUND
    )

@api.route('/api/customers', methods=["POST"])
def create_new_customer():
    data: dict = request.get_json()

    if data.get("name") is None or data.get("name").strip() == '':
        return (
            { 'message': 'O campo \"name\" é obrigatório.' },
            HTTPStatus.UNPROCESSABLE_ENTITY
        )
    
    if data.get('cpf') is None or data.get('cpf').strip() == '':
        return (
            { 'message': 'O campo \"cpf\" é obrigatório.' },
            HTTPStatus.UNPROCESSABLE_ENTITY
        )
    
    if len(data.get('cpf')) != 11:
        return (
            { 'message': 'O campo \"cpf\" deve conter 11 digitos.' },
            HTTPStatus.UNPROCESSABLE_ENTITY
        )
    
    try:
        birth_date = dt.datetime.strptime(data.get('birth_date'), '%Y-%m-%d')
    except:
        return (
            { 'message': 'O campo \"birth_date\" está inválido.' },
            HTTPStatus.UNPROCESSABLE_ENTITY
        ) 
    
    new_customer = {
        "id": generate_new_id(),
        "nome": data.get('name'),
        "cpf": data.get('cpf'),
        "data_nascimento": birth_date.date()
    }
    customers.append(new_customer)
    return (new_customer, HTTPStatus.CREATED)

@api.route('/api/customers/<int:id>', methods=["PUT"])
def update_customer(id: int):
    for customer in customers:
        if customer.get('id') == id:
            data: dict = request.get_json()

            if data.get("name") is None or data.get("name").strip() == '':
                return (
                    { 'message': 'O campo \"name\" é obrigatório.' },
                    HTTPStatus.UNPROCESSABLE_ENTITY
                )
            
            if data.get('cpf') is None or data.get('cpf').strip() == '':
                return (
                    { 'message': 'O campo \"cpf\" é obrigatório.' },
                    HTTPStatus.UNPROCESSABLE_ENTITY
                )
            
            if len(data.get('cpf')) != 11:
                return (
                    { 'message': 'O campo \"cpf\" deve conter 11 digitos.' },
                    HTTPStatus.UNPROCESSABLE_ENTITY
                )
            
            try:
                birth_date = dt.datetime.strptime(data.get('birth_date'), '%Y-%m-%d')
            except:
                return (
                    { 'message': 'O campo \"birth_date\" está inválido.' },
                    HTTPStatus.UNPROCESSABLE_ENTITY
                ) 
            
            new_customer = {
                "nome": data.get('name'),
                "cpf": data.get('cpf'),
                "data_nascimento": birth_date.date()
            }

            customer.update(new_customer)
            return (customer, HTTPStatus.ACCEPTED)

    return (
        { 'message': 'Cliente não encontrado' }, 
        HTTPStatus.NOT_FOUND
    )

@api.route('/api/customers/<int:id>', methods=["DELETE"])
def delete_customer(id: int):
    for idx, customer in enumerate(customers):
        if customer.get('id') == id:
            customers.pop(idx)
            return (
                { 'message': 'Cliente foi excluido com sucesso.' }, 
                HTTPStatus.ACCEPTED
            )

    return (
        { 'message': 'Cliente não encontrado' }, 
        HTTPStatus.NOT_FOUND
    )