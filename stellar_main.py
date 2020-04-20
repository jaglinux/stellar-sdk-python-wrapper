from stellar_sdk import Server, Keypair, TransactionBuilder, Network
import requests
from flask import Flask
from flask_cors import CORS
from flask import jsonify

app = Flask(__name__)
CORS(app)

class stellarWrapper:
    def __init__(self, network='test'):
        if network == 'test':
            self.server = Server("https://horizon-testnet.stellar.org")

    @staticmethod
    def create_account():
        kp = Keypair.random()
        print("Public Key is " + kp.public_key)
        print("Secret Seed is " + kp.secret)
        return kp

    @staticmethod
    def fund_test_account(publicKey):
        url = 'https://friendbot.stellar.org'
        res = requests.get(url, params={'addr': publicKey})
        print(res)

    def load_account(self, publicKey):
        account = self.server.load_account(publicKey)
        print(account)
        return account

    def load_server_account(self, publicKey):
        accountDetails = self.server.accounts().account_id(publicKey).call()
        print(accountDetails)
        return accountDetails

    def load_threshold(self, publicKey):
        accountDetails = self.load_server_account(publicKey)
        return accountDetails['thresholds']

    def load_native_balance(self, publicKey):
        accountDetails = self.load_server_account(publicKey)
        for x in accountDetails['balances']:
            if x['asset_type'] == 'native':
                return x['balance']

    def load_sequence(self, publicKey):
        accountDetails = self.load_server_account(publicKey)
        return accountDetails['sequence']

    def create_transaction(self, publicKey, operationList):
        sourceAccount = self.load_account(publicKey)
        transactionBuilder = TransactionBuilder(
            source_account=sourceAccount,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE)
        transaction = transactionBuilder.build()
        return transaction.to_xdr()


@app.route('/')
def main():
    answer = {}
    stellar = stellarWrapper()
    kp = stellar.create_account()
    stellar.fund_test_account(kp.public_key)
    stellar.load_account(kp.public_key)
    accountDetails = stellar.load_server_account(kp.public_key)
    thresh = stellar.load_threshold(kp.public_key)
    balance = stellar.load_native_balance(kp.public_key)
    seq = stellar.load_sequence(kp.public_key)
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
