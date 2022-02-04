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

DEBUG = True

relays = ['0x69429FB223b3BA3D5823B980E590bF857a680c13']

shepherds = ['0xb43114Bd08B4583b2a7e3ae4603831AB5fa6711f']

tags = [
	#'init',
	#'dog',
	'cat',
	#'fox',
	#'pelii'
]

w3_providers = ['https://rinkeby.infura.io/v3/4ac3bf1caeb14c3e9c241c25ea1d3326']
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
	w3 = Web3(Web3.HTTPProvider(w3_providers[0]))

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
        if DEBUG:
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
# Primary OpCodes
###################

def c0_Seconday_OpCodes(cmd):
	if DEBUG: log('0_Seconday_OpCodes: '+str(cmd), debug=True)
	pass

def c1_Add_Tag(cmd):
	if DEBUG: log('1_Add_Tag: '+str(cmd), debug=True)
	pass
def c2_Remove_Tag(cmd):
	if DEBUG: log('2_Remove_Tag: '+str(cmd), debug=True)
	pass

def c3_Add_Shepherd(cmd):
	if DEBUG: log('3_Add_Shepherd: '+str(cmd), debug=True)
	pass
def c4_Remove_Shepherd(cmd):
	if DEBUG: log('4_Remove_Shepherd: '+str(cmd), debug=True)
	pass

def c5_Add_Relay(cmd):
	if DEBUG: log('5_Add_Relay: '+str(cmd), debug=True)
	pass
def c6_Remove_Relay(cmd):
	if DEBUG: log('6_Remove_Relay: '+str(cmd), debug=True)
	pass

def c7_Add_W3(cmd):
	if DEBUG: log('7_Add_W3: '+str(cmd), debug=True)
	pass
def c8_Remove_W3(cmd):
	if DEBUG: log('8_Remove_W3: '+str(cmd), debug=True)
	pass

def c9_Poll_Rate(cmd):
	if DEBUG: log('9_Poll_Rate: '+str(cmd), debug=True)
	pass


def Route_Command(cmd):
	opcode = cmd[1].split('~')[0]

	if opcode == '0':
		c0_Seconday_OpCodes(cmd)

	if opcode == '1':
		c1_Add_Tag(cmd)

	if opcode == '2':
		c2_Remove_Tag(cmd)

	if opcode == '3':
		c3_Add_Shepherd(cmd)

	if opcode == '4':
		c4_Remove_Shepherd(cmd)

	if opcode == '5':
		c5_Add_Relay(cmd)

	if opcode == '6':
		c6_Remove_Relay(cmd)

	if opcode == '7':
		c7_Add_W3(cmd)

	if opcode == '8':
		c8_Remove_W3(cmd)

	if opcode == '9':
		c9_Poll_Rate(cmd)


###################
# Web3
###################

relay_abi = [{"inputs":[],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_posthash","type":"bytes32"}],"name":"get_post","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_poster","type":"address"},{"internalType":"string","name":"_tag","type":"string"}],"name":"get_postcount_from_address_tag","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_poster","type":"address"},{"internalType":"string","name":"_tag","type":"string"},{"internalType":"uint256","name":"_id","type":"uint256"}],"name":"get_posthash_from_address_tag_id","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_poster","type":"address"},{"internalType":"string","name":"_tag","type":"string"}],"name":"get_posthashes_from_address_tag","outputs":[{"internalType":"bytes32[]","name":"","type":"bytes32[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"info","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"info_burn","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"info_contract_address","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_message","type":"string"},{"internalType":"string[]","name":"_tags","type":"string[]"}],"name":"push_post","outputs":[],"stateMutability":"nonpayable","type":"function"}]

def Get_Relay(address):
	return Web3.toChecksumAddress(address)

def Check_Post_Count(relay_contract, shepherd, tag):
	post_count = relay_contract.functions.get_postcount_from_address_tag(Web3.toChecksumAddress(shepherd), tag).call()
	return post_count

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
		# Poll messages for each relay -> shepherd -> tag
		for relay in relays:
			for shepherd in shepherds:
				for tag in tags:
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

					# Read and Process New Commands
					while Command_Count[sig] < count:
						new_index = Command_Count[sig] + 1
						cmd_data = Get_Command(relay_contract, shepherd, tag, new_index)
						print_cmd_info(cmd_data, relay, shepherd, tag, w3_providers[0], new_index)

						Command_Count[sig] = new_index

						Save_Command(cmd_data)
						Route_Command(cmd_data)

		time.sleep(POLL_RATE)

###################
# Start
###################

SCR_Listener()
