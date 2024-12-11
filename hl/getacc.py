import json
import os
import logging

import eth_account
from eth_account.signers.local import LocalAccount

from hyperliquid.exchange import Exchange
from hyperliquid.utils import constants
from hyperliquid.info import Info

# info = Info(constants.TESTNET_API_URL, skip_ws=True)
# user_state = info.user_state("0xcd5051944f780a621ee62e39e493c489668acf4d")
# print(user_state)


def setup(base_url=None, skip_ws=False, testnet:bool=True):

    # load account 
    account: LocalAccount = eth_account.Account.from_key(os.environ['HL_PRIVATEKEY'])
    address = os.environ['HL_TESTNETKEY'] if testnet else os.environ['HL_PUBLICKEY']

    if address == "":
        address = account.address
    logging.info("Running with account address:", address)
    if address != account.address:
        logging.info("Running with agent address:", account.address)

    info = Info(constants.TESTNET_API_URL if testnet else base_url, skip_ws)

    user_state = info.user_state(address)
    print(user_state)
    spot_user_state = info.spot_user_state(address)
    margin_summary = user_state["marginSummary"]

    #check account liquidity
    if float(margin_summary["accountValue"]) == 0 and len(spot_user_state["balances"]) == 0:
        logging.info("Not running the example because the provided account has no equity.")
        url = info.base_url.split(".", 1)[1]
        error_string = f"No accountValue:\nIf you think this is a mistake, make sure that {address} has a balance on {url}.\nIf address shown is your API wallet address, update the config to specify the address of your account, not the address of the API wallet."
        logging.error(error_string)
        raise Exception(error_string)

    exchange = Exchange(account, base_url, account_address=address)

    return address, info, exchange

# TODO: Add support for multiple wallet setup
# def setup_multi_sig_wallets():
#     config_path = os.path.join(os.path.dirname(__file__), "config.json")
#     with open(config_path) as f:
#         config = json.load(f)

#     authorized_user_wallets = []
#     for wallet_config in config["multi_sig"]["authorized_users"]:
#         account: LocalAccount = eth_account.Account.from_key(wallet_config["secret_key"])
#         address = wallet_config["account_address"]
#         if account.address != address:
#             raise Exception(f"provided authorized user address {address} does not match private key")
#         print("loaded authorized user for multi-sig", address)
#         authorized_user_wallets.append(account)
#     return authorized_user_wallets


if __name__ == "__main__": 
    address, info, exchange = setup(None,False,True)
    print(address, info, exchange)