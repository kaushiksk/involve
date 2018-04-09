# Involve - Ballot papers on ethereum smart contracts
Bringing transparency and security to voting using the ethereum blockchain.

# How it works
- Every time a vote is cast, a new smart contract is deployed on the ethereum blockchain. This 
  contains the constituency and the candidate that was voted for.
- The address of every contract is stored and made publicly available
- Anybody can read the data by accessing the smart contract using this address, which ensures complete transparency
  in vote counting and results and every vote cast is now accounted for.

# Technologies Used
 - __`[ganache-cli](https://github.com/trufflesuite/ganache-cli/)`__  : It provides a local ethereum network for us to interact with.
 - `web3.py` : Python wrapper around __Web3.js__. It helps us connect to the ethereum network and deploy smart contract or make transactions

Using the [Flat UI](https://designmodo.github.io/Flat-UI/) theme.

