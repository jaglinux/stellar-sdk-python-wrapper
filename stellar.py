from stellar_sdk import Server, Keypair, TransactionBuilder, Network, TransactionEnvelope, Transaction
import operation as op
import requests

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

    def get_threshold(self, publicKey):
        accountDetails = self.load_server_account(publicKey)
        return accountDetails['thresholds']

    def get_native_balance(self, publicKey):
        accountDetails = self.load_server_account(publicKey)
        for x in accountDetails['balances']:
            if x['asset_type'] == 'native':
                return x['balance']

    def get_sequence(self, publicKey):
        accountDetails = self.load_server_account(publicKey)
        return accountDetails['sequence']

    def create_transaction(self, sourceAccountPublicKey, operationList):
        sourceAccount = self.load_account(sourceAccountPublicKey)
        transactionBuilder = TransactionBuilder(
            source_account=sourceAccount,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE)
        #for operation in operationList:
        #    transactionBuilder.append_operation(operation)
        txnEnv = transactionBuilder.build()
        return txnEnv.to_xdr()

    @staticmethod
    def signTransaction(txnXdr, signature):
        txnEnv = TransactionEnvelope.from_xdr(txnXdr)
        txnEnv.sign(signature)
        txnEnv.to_xdr()

    def submitTransaction(self, txnXdr):
        txnEnv = Transaction.from_xdr(txnXdr)
        res = self.server.submit_transaction(txnEnv)
        print(res)
        return res
