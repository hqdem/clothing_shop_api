import uuid

from yookassa import Configuration, Payment

Configuration.account_id = '981495'
Configuration.secret_key = 'test_g9tzQTaNrJUz2WJyryMECyeuzSzuhYjdBKsfAiV-YS8'


def create_payment(amount):
    idempotence_key = str(uuid.uuid4())

    payment = Payment.create({
        "amount": {
            "value": f"{amount}",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": f"http://localhost:8000/api/v1/orders/confirm_payment/"
        },
        "capture": True,
        "description": "Заказ №1"
    }, idempotence_key)
    return payment


def find_payment(payment_id):
    return Payment.find_one(payment_id)
