from stellar_sdk import operation

def add_payment_op(source_account, destination_account, asset, amount):
    op = operation.payment(destination_account, asset, amount, source_account)
    return op
