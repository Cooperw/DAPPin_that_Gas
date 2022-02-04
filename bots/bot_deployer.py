'''
a. shiloh
'''

#############
# Imports
#############
import os
import signal
import subprocess
import sys

#############
# Variables
#############
Bot_Pids = []

#############
# Helpers
#############
def Usage():
	print('Usage: '+sys.argv[0]+' <num bots> <bot script>')
	exit(1)

#############
# Main
#############
def Manage_Bots():
	Spawn_Bots()
	print('Spawned '+str(len(Bot_Pids))+' bots.')
	input("Press Enter to kill bots...")
	Kill_Bots()

def Spawn_Bots():
	for x in range(0, num_bots):
		args = ['python3', bot_script]
		bot = subprocess.Popen(args=args)
		Bot_Pids.append(bot.pid)

def Kill_Bots():
	for bot_pid in Bot_Pids:
		os.kill(bot_pid, signal.SIGTERM)

#############
# Start
#############
if __name__ == '__main__':
	try:
		num_bots = int(sys.argv[1])
		bot_script = sys.argv[2]
	except:
		Usage()

	Manage_Bots()
