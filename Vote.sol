// Declare the source file compiler version
pragma solidity ^0.4.19;

contract Vote {
    /* Define variable owner of the type address
       and data as an array of byte32
       This is because web3.py does not yet allow passing strings as arguments to constructor */
    address owner;
    bytes32[] data;
    /* This function is executed at initialization */
    function Vote(bytes32 constituency, bytes32 candidate) public { 
            owner = msg.sender;
            data.push(constituency);
            data.push(candidate);
        }
    
    function info() public view returns(bytes32[]) {
        return data;
    }

}