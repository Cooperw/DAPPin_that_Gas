# DAPPin that A$$ | A Blockchain Enabled C2 Solution


A C2 solution that lives in the blockchain as a DAPP.

Core Contents:
* [SpectralCommandRelay.sol](SpectralCommandRelay.sol): Smart Contract that can be deployed to the blockchain to act as a C2 channel
* [bot_deployer.py](bot_deployer.py): Script that generates & manages a local botnet
* [bot_minimal.py](bot_minimal.py): An incredibly simple endpoint for our C2 blockchain solution to be run on infected devices
* [bot.py](bot.py): Template for a more advanced endpoint for our C2 blockchain solution to be run on infected devices

Demo Contents:
* [SCR_Demo_Meter.rc](SCR_Demo_Meter.rc): MSFConsole init script used in our local botnet demo
* [cleanup.sh](cleanup.sh): Script to cleanup any lingering meterpreter sessions after our demo

Presentation Contents
* [DAPPin_that_A$$_DEFCON_Submission_BlockchainC2.pptx](DAPPin_that_A$$_DEFCON_Submission_BlockchainC2.pptx): The powerpoint we sent to the DEFCON Talks Panel
