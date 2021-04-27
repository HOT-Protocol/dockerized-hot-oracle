# dockerized-hot-oracle

## Summary
Using docker to start HOT/GBP Oracle client quickly

## Quick start
1. generate configuration file
```
python generator.py

1. Please choice network (mainnet, ropsten, kovan, rinkeby, goerli): kovan
2. Please enter oracle address [0x]: 0x0000000000000000000000000000000000000000
3. Please enter your <INFURAKEY>(https://infura.io): 935a2863572e43f7aea5a80029a7bd1e
4. Please enter wallet keystore: {"id":"****************","address":"****************","version":3,"crypto":{"cipher":"aes-128-ctr","kdfparams":{"r":8,"salt":"****************","dklen":32,"p":1,"n":262144},"mac":"****************","cipherparams":{"iv":"****************"},"ciphertext":"****************","kdf":"scrypt"}}
5. Please enter keystore unlock password: 123456

Successful!!!
```

2. deploy and run docker container
``` shell
python deploy.py
```