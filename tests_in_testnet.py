import json
from turtle import delay
from Crypto.Hash import keccak
from web3 import Web3
from eth_account.messages import encode_defunct
from random import randint
import time

node_link = "https://ropsten.infura.io/v3/8fb4ff34af8c495db885ff26dccdf05e" 
w3 = Web3(Web3.HTTPProvider(node_link))

vault_account = "0xB3FbdBDc07D50812c955b70AF7D8a094b18319Cd"
RobotParts_abi = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256[]","name":"ids","type":"uint256[]"},{"indexed":false,"internalType":"uint256[]","name":"values","type":"uint256[]"}],"name":"TransferBatch","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"TransferSingle","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"value","type":"string"},{"indexed":true,"internalType":"uint256","name":"id","type":"uint256"}],"name":"URI","type":"event"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"id","type":"uint256"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"accounts","type":"address[]"},{"internalType":"uint256[]","name":"ids","type":"uint256[]"}],"name":"balanceOfBatch","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256[]","name":"ids","type":"uint256[]"},{"internalType":"uint256[]","name":"amounts","type":"uint256[]"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"mintBatch","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"mintToken","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256[]","name":"ids","type":"uint256[]"},{"internalType":"uint256[]","name":"amounts","type":"uint256[]"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"safeBatchTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"newuri","type":"string"}],"name":"setURI","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"uri","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"}]')
Rewarder_abi = json.loads('[{"inputs":[{"internalType":"address","name":"robotparts","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"newStorage_","type":"address"}],"name":"changeDropStorage","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getSessionId","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"session","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"server1_","type":"address"}],"name":"setServer1","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"server2_","type":"address"}],"name":"setServer2","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"uint8[5]","name":"rewards","type":"uint8[5]"},{"internalType":"address","name":"address_","type":"address"},{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"bytes","name":"sign","type":"bytes"}],"internalType":"struct RewarderManager.transaction[]","name":"_txs","type":"tuple[]"},{"internalType":"bytes","name":"sign","type":"bytes"}],"name":"unstorage","outputs":[],"stateMutability":"nonpayable","type":"function"}]')

#constants*
RobotParts_address = "0x81a0Cd24fE569F825559eD2CD44E0385562CA9aB"
Rewarder_address = "0xd5Bc25dcB0197637aC41Fa4ec6aFC1487be681Ef"

RobotPart = w3.eth.contract(address = RobotParts_address, abi = RobotParts_abi)
Rewarder = w3.eth.contract(address = Rewarder_address, abi = Rewarder_abi)

#constants
CORE_SERVER = "0x983bE8102b0B68be2a9c80Ac17ED6f21571dD33d" #serServer1
CORE_SERVER_PRIVATE_KEY = "426aff1be66abf441840ee992d6c902b7a81df527b5cee6a5d71c33663a35e8b"
OPER_SERVER = "0xCFCe125E19459ce898c9d82f3E2aB63922a56057" #setSetver2
OPER_SERVER_PRIVATE_KEY = "aa70a709411afc44d1a6db05aa2d0f89d0b4ad27996ec6e2ea0f61309472858e" 
player_1_address = ""
player_1_private_key = ""

AMOUNT_ROBOTPARTS = 5
INT_SIZE = 8 # ellement size of uint array in contract structure

def getAmountRobotParts (player):
    addresses = [player] * AMOUNT_ROBOTPARTS
    ids = list(range(AMOUNT_ROBOTPARTS))
    r = RobotPart.functions.balanceOfBatch(addresses, ids).call()
    return r


class tx:
    def __init__(self, rewards_, player_, addressNFT_ = "0x0000000000000000000000000000000000000000", id_ = 0):
        self.rewards = rewards_
        self.player_address = player_
        self.addressNFT = addressNFT_
        self.id = id_
        self.sign = ""

    def tx_message(self):
        session = Rewarder.functions.getSessionId(self.player_address).call()
        #Вот эту функцию явно можно переписать лучше
        return intArrayToByteString(self.rewards) + self.addressNFT[2:] + ("0" * (256 // 4  - len(hex(self.id)[2:]))) + hex(self.id)[2:] + self.player_address[2:] + ("0" * (256 // 4  - len(hex(session)[2:]))) + hex(session)[2:]


    def updateSign(self):
        msg_hash = encode_defunct(hexstr = keccak256(self.tx_message()))
        self.sign = w3.eth.account.sign_message(msg_hash, OPER_SERVER_PRIVATE_KEY).signature.hex()

    def getTuple(self):
        return (self.rewards, self.addressNFT, self.id, self.sign)

def keccak256 (s):
    #Тут импортирован класс Kecak256, но с ним я пока не разобрался, пока использую это
    return keccak.new(data= bytes.fromhex(s), digest_bits=256).digest().hex()

def intArrayToByteString(a: list):
    r = ""
    for i in a:
        r += "0" * (INT_SIZE // 4  - len(str(hex(i)[2:]))) + str(hex(i)[2:])
    return r

def createReward(rewards_: list, player_: str):
    r = tx(rewards_, player_)
    r.updateSign()
    return r

def getGeneralSign(txs): #возвращает обущую сигну от основногго сервера
    msg = ""
    for i in txs:
        msg += i.sign[2:]
    msg_hash = encode_defunct(hexstr = keccak256(msg))
    return w3.eth.account.sign_message(msg_hash, CORE_SERVER_PRIVATE_KEY).signature.hex()
    

#разные тесты
print(getAmountRobotParts(player_1_address))
for i in range(3, 15):
    rewards_for_player_1 = [createReward([randint(1,20) for k in range(5)], player_1_address), createReward([randint(1,20) for k in range(5)], player_1_address)]
    nonce = w3.eth.getTransactionCount(player_1_address)
    tx_ = Rewarder.functions.unstorage([r.getTuple() for r in rewards_for_player_1], getGeneralSign(rewards_for_player_1)).buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": 3,
            "from": player_1_address,
            "nonce": nonce
        }
    )
    signed_tx = w3.eth.account.sign_transaction(tx_, private_key = player_1_private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt =w3.eth.wait_for_transaction_receipt(tx_hash)
    print(getAmountRobotParts(player_1_address))
    time.sleep(15)
    
