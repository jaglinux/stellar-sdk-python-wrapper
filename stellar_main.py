from stellar_sdk import Server, Keypair, TransactionBuilder, Network
import requests

server = Server("https://horizon-testnet.stellar.org")

def test():
	base_fee = server.fetch_base_fee()
	print(base_fee)

def create_account():
	kp = Keypair.random()
	print("Public Key is " + kp.public_key)
	print("Secret Seed is " + kp.secret)
	return kp

def fund_test_account(publicKey):
	url = 'https://friendbot.stellar.org'
	res = requests.get(url, params={'addr' : publicKey})
	print(res)

def load_account(publicKey):
	acc_resp = server.load_account(publicKey)
	print(acc_resp)
	return acc_resp

def load_server_account(publicKey):
	acc_resp = server.accounts().account_id(publicKey).call()
	print(acc_resp)
	return acc_resp

def load_threshold(publicKey):
	acc_resp = load_server_account(publicKey)
	return acc_resp['thresholds']

def load_native_balance(publicKey):
	acc_resp = load_server_account(publicKey)
	for x in acc_resp['balances']:
		if x['asset_type'] == 'native':
			return x['balance']

def load_sequence(publicKey):
	acc_resp = load_server_account(publicKey)
	return acc_resp['sequence']

def create_transaction(publicKey, operationList):
	sourceAccount = load_account(publicKey)
	transactionBuilder = TransactionBuilder(
		source_account=sourceAccount,
		network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE)
	transaction = transactionBuilder.build()
	return transaction.to_xdr()

if __name__ == '__main__':
	test()
	kp = create_account()
	fund_test_account(kp.public_key)
	load_account(kp.public_key)
	acc_resp = load_server_account(kp.public_key)
	thresh = load_threshold(kp.public_key)
	print("------------Threshold is ", thresh)
	balance = load_native_balance(kp.public_key)
	print("------------Balance is ", balance)
	seq = load_sequence(kp.public_key)
	print("------------Sequence is ", seq)
	txn_xdr = create_transaction(kp.public_key, None)
	print("------------Txn xdr is ", txn_xdr)


