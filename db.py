import datetime as dt


customers = [
    {
        "id": 1,
        "nome": "Davi",
        "cpf": "12354667644",
        "data_nascimento": dt.date(2004, 1, 14)
    },
    {
        "id": 2,
        "nome": "Fernanda",
        "cpf": "12354667643",
        "data_nascimento": dt.date(1997, 11, 22)
    }
]


def generate_new_id():
    global customers
    ids = [customer.get('id') for customer in customers]
    return max(ids) + 1
