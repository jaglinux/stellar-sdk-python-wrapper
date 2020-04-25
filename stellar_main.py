from flask import Flask
from flask_cors import CORS
from flask import jsonify
from stellar import stellarWrapper

app = Flask(__name__)
CORS(app)

@app.route('/')
def main():
    answer = {}
    stellar = stellarWrapper()
    kp = stellar.create_account()
    stellar.fund_test_account(kp.public_key)
    stellar.load_account(kp.public_key)
    accountDetails = stellar.load_server_account(kp.public_key)
    thresh = stellar.get_threshold(kp.public_key)
    balance = stellar.get_native_balance(kp.public_key)
    seq = stellar.get_sequence(kp.public_key)
    txn_xdr = stellar.create_transaction(kp.public_key, None)
    answer["Public_Key"] = kp.public_key
    answer["Threshold"] = thresh
    answer["Balance"] = balance
    answer["Sequence"] = seq
    answer["Txn XDR"] = txn_xdr

    print("------------Threshold is ", thresh)
    print("------------Balance is ", balance)
    print("------------Sequence is ", seq)
    print("------------Txn xdr is ", txn_xdr)
    return jsonify(answer), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')
