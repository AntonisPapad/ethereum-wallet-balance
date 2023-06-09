import re
from alchemy import Alchemy, Network
from pprint import pprint
from web3 import Web3
from coinmarketcap_func import get_crypto_prices
from config import ALCHEMY_API_KEY


def is_valid_symbol(symbol):
    return re.match("^[A-Za-z0-9]+$", symbol) is not None


def create_web3_object():
    alchemy_url = f"https://eth-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}"
    return Web3(Web3.HTTPProvider(alchemy_url))


def get_eth_balance(address, alchemy, w3):
    wei_balance = alchemy.core.get_balance(address)
    eth_balance = w3.from_wei(wei_balance, "ether")
    return float(eth_balance)


def get_token_balances(address, network_name, w3):
    # create Alchemy object for specified network
    network_obj = getattr(Network, network_name)
    alchemy = Alchemy(ALCHEMY_API_KEY, network_obj)

    # Get ETH balance
    eth_balance = get_eth_balance(address, alchemy, w3)

    # Get token balances
    tokens = alchemy.core.get_token_balances(address)
    tokens = [token for token in tokens['token_balances']]

    token_list = []
    # Loop through all tokens with non-zero balance
    for token in tokens:
        # Get balance of token
        balance = token.token_balance

        # Get metadata of token
        metadata = alchemy.core.get_token_metadata(token.contract_address)

        if metadata.decimals and metadata.symbol is not None and is_valid_symbol(metadata.symbol):
            # Compute token balance in human-readable format
            balance = w3.to_int(hexstr=balance) / \
                pow(10, metadata.decimals)

            if balance > 0:

                balance = round(balance, 5)

                token_list.append({
                    "name": metadata.name,
                    "symbol": metadata.symbol,
                    "balance": balance,
                    "logo": metadata.logo
                })

    symbol_list = [token["symbol"] for token in token_list]

    if symbol_list:  # If symbol_list is not empty
        prices = get_crypto_prices(symbol_list)

        for token in token_list:
            try:
                token["price"] = prices[token["symbol"]]
            except KeyError:
                token_list.remove(token)

    return token_list


def main():
    address = input("Enter Ethereum address: ")

    w3 = create_web3_object()
    # Check if address is valid
    if not w3.is_address(address):
        print("Invalid Ethereum address")
        return

    # networks = ["ETH_MAINNET", "ARB_MAINNET", "OPT_MAINNET"]
    networks = ["ETH_MAINNET"]
    for network in networks:
        pprint(f"Network: {network}")
        pprint(get_token_balances(address, network, w3))


if __name__ == "__main__":
    main()
