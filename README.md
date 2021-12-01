# stellar-implimentation
move money and access new markets.
intended to enhance rather than undermine or replace the existing financial system.

A valid keypair does not make an account: in order to prevent unused accounts from bloating the ledger, Stellar requires accounts to hold a minimum balance of 1 XLM before they actually exist. Until it gets a bit of funding, your keypair doesn’t warrant space on the ledger.

git clone https://github.com/StellarCN/py-stellar-base.git
cd py-stellar-base
pip install .

Create a token:

1. You need at least 5 XLM in an active wallet to create your own Asset on the network.
2. You're going to be creating 2 Stellar accounts in order to generate you're own asset:
Issuer account - is kept separate from the account you'll use to distribute your new Asset. This makes it easy for you to prove to the world the economics behind your asset. Lock the issuer account after creating a fixed number of tokens, and this lets the world know that no more of your tokens can ever be created.
Distributor account - receives tokens from the Issuer account, and is the account you will then use to distribute your tokens to other Stellar wallets etc.

