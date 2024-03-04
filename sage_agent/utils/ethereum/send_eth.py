from eth_account import Account
from eth_typing import Address
from web3 import Web3
from web3.types import TxReceipt

from sage_agent.utils.ethereum.constants import GAS_PRICE_MULTIPLIER


def send_eth(account: Account, to: str, value: int, web3: Web3) -> tuple[str, TxReceipt]:
    bytes_address: Address = Address(bytes.fromhex(account.address[2:]))

    nonce = web3.eth.get_transaction_count(bytes_address)

    tx = {
        'from': account.address,
        'to': to,
        'value': value,
        'gasPrice': int(web3.eth.gas_price * GAS_PRICE_MULTIPLIER),
        'nonce': nonce,
        'chainId': web3.eth.chain_id
    }

    gas = web3.eth.estimate_gas(tx)
    tx.update({'gas': gas})

    signed_tx = account.sign_transaction(tx)

    web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    print("Send ETH (" + str(int(value / 10 ** 18)) + ") TX: ", signed_tx.hash.hex())

    receipt = web3.eth.wait_for_transaction_receipt(signed_tx.hash)

    return receipt["transactionHash"].hex(), receipt