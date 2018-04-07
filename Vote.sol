// Declare the source file compiler version
pragma solidity ^0.4.19;

contract Vote {
    /* Define variable owner of the type address */
    address owner;
    bytes32[] data;
    /* This function is executed at initialization and sets the owner of the contract */
    function Vote(bytes32 constituency, bytes32 candidate) public { 
            owner = msg.sender;
           data.push(constituency);
           data.push(candidate);
        }
    
    function info() public view returns(bytes32[]) {
        return data;
    }

}
