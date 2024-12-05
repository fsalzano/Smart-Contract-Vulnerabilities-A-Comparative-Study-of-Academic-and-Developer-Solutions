## Table of content
- Guideline from Defining Smart Contract Defects on Ethereum (Chen et al.) [1]
- Guideline from SGUARD:TowardsFixingVulnerableSmart ContractsAutomatically (Chen et al.) [2]
Patching arithmetic
Patching Reentrancy
- Security Code Recommendations for Smart Contract (Zhou et al.)  [3]
Illegal Coverage
Reentrancy
Incorrect Inheritance Order
Authorization Through tx.origin
Missing Return Statement
Use of Deprecated Functions
Erroneous Visibility
Unchecked Return Value
Arithmetic Issue
Erroneous Variable Type
Solidity Keyword Addition
SafeMath Library Use
- Tips: towards automating patch suggestion for vulnerable smart contracts (Chen et al.) [4]
Fixing unchecked external calls.
Fixing reentrancy.
Fixing access control.
Fixing arithmetic issue.
Fixing strict balance equality.
Fixing unmatched type assignment.
Inserting a suicide function.
Fixing hard coded address.
- Smart Contract Code Repair Recommendation based on Reinforcement Learning  [5]
References

Guideline from Defining Smart Contract Defects on Ethereum (Chen et al.) [1]

(1) Unchecked External Calls: To transfer Ethers or call functions of other smart contracts, Solidity provides a series of external call functions for raw addresses, i.e., address.send(), address.call(), address.delegatecall(). Unfortunately, these methods may fail due to network errors or out-of-gas error, e.g., the 2300 gas limitation of fallback function introduced in Section 2. When errors happen, these methods will return a boolean value (False), but never throw an exception. If callers do not check return values of external calls, they cannot ensure whether code logic is correct. Example: An example of this defect is given in the snippet below. In function getWinner , the contract does not check the return value of send, but the array participants is emptied by assigning participatorID to 0. In this case, if the send method failed, the winner will lose 8 Ethers. Possible Solution: Using address.transfer() to instead address.send() and address.call.value() if possible, or checking the return value of send and call.


function getWinner() {
    uint256 winnerID = uint256(block.blockhash(block.number)) %
    participants.length;
    participants[winnerID].send(8 ether);
    participatorID = 0;
}
(2) DoS Under External Influence: When an exception is detected, the smart contract will roll back the transaction. However, throwing exceptions inside a loop is dangerous. Example: In line of the snippet below, the contract uses transfer to send Ethers. However, In Solidity, transfer and send will limit the gas of fallback function in callee contracts to 2,300 gas. This gas is not enough to write to storage, call functions or send Ethers. If one of member[i] is an attacker’s smart contract and the transfer function can trigger an out-of-gas exception due to the 2,300 gas limitation. Then, the contract state will roll back. Since the code cannot be modified, the contract cannot remove the attacker from members list, which means that if the attacker does not stop attacking, no one can get bonus anymore. Possible Solution: Avoid throwing exceptions in the body of a loop. We can return a boolean value instead of throwing an exception. For example, using “if(msg.send(...) == false) break;” instead of using “msg.transfer(...)”.


function giveBonus() returns(bool){ //send 0.1 ETH to all members as bonus 29 
    //Unmatched Type Assignment , Nested Call
    for(uint i = 0; i < members.length; i++){
        if( this.balance > 0.1 ether) 
        //DoS Under External Influence
            members[i].transfer (0.1 ether); } 
        //Missing Return Statement∗/ }
}
(3) Strict Balance Equality: Attackers can send Ethers to any contracts forcibly by utilizing selfdestruct(victim address) API. This way will not trigger the fallback function, meaning the victim contract cannot reject the Ethers. Therefore, the logic of equal balance check will fail to work due to the unexpected ethers sent by attackers. Example: Attackers can send 1 Wei (1 Ether = 10^18 Wei) to Contract Gamble in Listing 1 by utilizing selfdestruct method. This method will not trigger fallback function. Thus, the Ethers will not be thrown by ReceiveEth in the snippet below. If this attack happens, the getWinner()  would never be executed because the getWinner can only be executed when the balance of the contract is strictly equal to 10 Ethers. Possible Solution: Since the attackers can only add the amount of the balance, we can use a range to replace “==”. In this case, attackers cannot affect the logic of the programs. Using the defect in Listing 1 as an example, we can modify the code in to “if (this.balance ≥ 10 ether && this.balance < 11 ether)”


function ReceiveEth() payable{ 1
     if(msg.value!=1 ether){ 
         revert () ;}
    //msg.value is the number of received ETHs 
     members.push(msg.sender); 
     participators[participatorID] =msg.sender; 
     participatorID++;
     if( this .balance == 10 ether){
     //Strict Balance Equality
        getWinner();}
}
(4) Unmatched Type Assignment: Solidity supports different types of integers (e.g., uint8, uint256). The default type of integer is uint256 which supports a range from 0 to 2^256. uint8 takes less memory but only supports numbers from 0 to 2^8. Solidity will not throw an exception when a value exceeds its maximum value. The progressive increase is a common operation in programming, and performing an increment operation without checking the maximum value may lead to overflow. Example: The variable i in line 30 of the snippet below is assigned to uint8 because 0 is in the range of uint8 (0-255). If the members.length is larger than 255, the value of i after 255 is 0. Thus, the loop will not stop until running out of gas or the balance of the account is less than 0.1. Possible Solution: Using uint or uint256 if we are not sure of the maximum number of loop iterations.


function giveBonus() returns(bool){ //send 0.1 ETH to all members as bonus 29 
    //Unmatched Type Assignment , Nested Call
    for(uint i = 0; i < members. length; i++){
        if( this.balance > 0.1 ether) 
        //DoS Under External Influence
            members[i].transfer (0.1 ether); } 
        //Missing Return Statement∗/ }
}
(5) Transaction State Dependency: Contracts need to check whether the caller has permissions in some functions like suicide as the snippet below. The failure of permission checks can cause serious consequences. For example, if someone passes the permission check of suicide function, he/she can destroy the contract and steal all the Ethers. tx.origin can get the original address that kicked off the transaction, but this method is not reliable since the address returned by this method depends on the transaction state. Example:  The contract uses tx.origin to check whether the caller has permission to execute function suicide. However, if an attacker uses function attack  to call suicide function , the permission check will fail. The suicide function will check whether the sender has permission to execute this function. However, the address obtained by tx.origin is always the address who creates this contract. Therefore, anyone can execute the suicide function and withdraw all of the Ethers in the contract. Possible Solution: Using msg.sender to check the permission instead of using tx.origin.


modifier onlyOwner{//Transaction State Dependency // 
     require(tx.origin == owner); 
      _; }
      
function suicide(address addr) onlyOwner{ 
    //Remove the contract from blockchain 
     selfdestruct (addr);
}

function attack(address addr , address myAddr){ 
  Gamble gamble = Gamble(addr); 
  gamble.suicide(myAddr);}
}
(6) Block Info Dependency: Ethereum provides a set of APIs (e.g., block.blockhash, block.timestamp) to help smart contracts obtain block-related information, like timestamps or hash numbers. Many contracts use these pieces of block information to execute some operations. However, the miner can influence block information; for example, miners can vary block timestamp by roughly 900 seconds. In other words, block info dependency operations can be controlled by miners to some extent. Example: In the snippet below, the contract uses blockhash to generate which member is the winner. However, the gamble is not fair because miners can manipulate this operation. Possible Solution: To generate a safer random number in Solidity, we should ensure the random number cannot be controlled by a single person, e.g., a miner. We can use the information of users like their addresses as their input numbers, as their distributions are completely random. Also, to avoid attacks, we need to hide the values we used from other players. Since we cannot hide the address of users and their submitted values, a possible solution to generate a random number without using block-related APIs using a hash number. The algorithm has three rounds:

Round 1: Users obtain a random number and generate a hash value on their local machine. The hash value can be obtained by keccak256, which is provided by Solidity. After obtaining the random number, users submit the hash number.

Round 2: After all users submit their hash number, users are required to submit their original random number. The contract checks whether the original number can generate the same hash number.

Round 3: If all users submit the correct original numbers, the contract can use the original numbers to generate a random number.


function getWinner(){ //choose a member to be the winner 
 //Block Info Dependency
    uint winnerID = uint(block.blockhash(block.number)) % participants.length; 
    participants[winnerID].send(8 ether); 
    participatorID = 0;
}
(7) Re-entrancy: Concurrency is an important feature of traditional software. However, Solidity does not support it, and the functions of a smart contract can be interrupted while running. Solidity allows parallel external invocations using call method. If the callee contract does not correctly manage the global state, the callee contract will be attacked – called a re-entrancy attack. Example: The snippet below shows an example of re-entrancy. The Attacker contract invokes Victim contract’s withdraw() function in. However, Victim contract sends Ethers to attacker contract  before resetting the balance. Victim will invoke the fallback function  of attacker contract and lead to repeated invocation. Possible Solution: Using send() or transfer to transfer Ethers. send() and transfer have gas limitation of 2300 if the recipient is a contract account, which are not enough to transfer Ethers. Therefore, these two functions will not cause Re-entrancy.


contract Victim {
​
    mapping(address => uint) public userBalannce; 
​
    function withDraw(){ 
        uint amount = userBalannce[msg.sender ]; 
        if(amount>0){ 
            msg.sender.call.value(amount)() ; 
            userBalannce[msg.sender] = 0;}} ...} 
​
contract Attacker{ 
                 
    function() payable{ 
        Victim(msg.sender).withDraw() ;} 
                      
    function reentrancy(address addr){ 
        Victim(addr).withDraw() ;} 
    }
}
(8) Nested Call: Instruction CALL is very expensive (9000 gas paid for a non-zero value transfer as part of the CALL operation). If a loop body contains CALL operation but does not limit the number of times the loop is executed, the total gas cost would have a high probability of exceeding the gas limitation because the number of iterations may be high and it is hard to know its upper limit. Example: In the snippet below, the function giveBonus  uses transfer  which generates CALL to send Ethers. Since the members.length does not limit its size, giveBonus has a probability to cause out-of-gas error. When this error happens, this function cannot be called anymore because there is no way to reduce the members.length. Possible Solution: The developers should estimate the maximum number of loop iterations that can be supported by the contract and limit these loop iterations.


function giveBonus() returns(bool){ 
//send 0.1 ETH to all members as bonus  
//Unmatched Type Assignment , Nested Call
  for(var i = 0; i < members. length; i++){ 
     if(this.balance > 0.1 ether) 
      //DoS Under External Influence∗/ 
       members[i].transfer(0.1 ether); } 
       //Missing Return Statement∗/ }
}
(9) Misleading Data Location: In traditional programming languages like Java or C, variables created inside a function are local variables. Data is stored in memory, and the memory will be released after the function exits. In Solidity, the data of struct, mapping, arrays are stored in storage even if they are created inside a function. However, since storage in Solidity is not dynamically allocated, storage variables created inside a function will point to the storage slot 50 by default. This can cause unpredictable bugs. Example: Function reAssignArray  in the snippet below creates a local variable tmp. The default data location of tmp is storage, but EVM cannot allocate storage dynamically. There is no space for tmp, but instead, it will point to the storage slot 0. For the result, once function reAssignArray is called, the variable variable will add 1, which can cause bugs for the contract. Possible Solution: Clarifying the data location of struct, mapping, and arrays if they are created inside a function.


function reAssignArray(){
    /∗Misleading Data Location∗/ 
    uint [] tmp; 
    tmp.push(0) ; 
    investList = tmp;
}
Guideline from SGUARD:TowardsFixingVulnerableSmart ContractsAutomatically (Chen et al.) [2]

Patching arithmetic

The result of patching are in the function transferProxyPatched. Almost all arithmetic operations (in statements or expressions) are replaced with function calls that perform the corresponding operations safely (i.e., with proper checks for arithmetic overflow or underflow).

function transferProxy(address from, address to, uint value, uint fee) public { 
    if (balances[from] < fee + value) revert(); 
    uint nonce=nonces[from]; 
    if (balances[to] + value < balances[to]) revert(); 
    if (balances[msg.sender] + fee < balances[msg.sender ]) revert(); 
    balances[to] += value; 7 balances[msg.sender] += fee; 
    balances[from] -= value + fee; 
    nonces[from] = nonce + 1; 
}
function transferProxyPatched(address from, address to,uint value, uint fee) public { 
    if (balances[from] < add_uint256(fee, value)) revert (); 
    uint nonce = nonces[from]; 
    if (add_uint256(balances[to], value) < balances[to]) revert(); 
    if (add_uint256(balances[msg.sender],fee) < balances [msg.sender]) revert(); 
    balances[to] = add_uint256(balances[to], value); 
    balances[msg.sender] = add_uint256(balances[msg. sender],fee); 
    balances[from] = sub_uint256(balances[from], add_uint256(_value,fee)) 
    nonces[from] = nonce +1; 
}
Patching Reentrancy

The result of patching are in the function burnPatched. nonReentrant modifier from OpenZeppelin is used.

function getThisWeekBurnedAmount() public view returns( uint){
    uint thisWeekStartTime=getThisWeekStartTime(); 
    uint total=0; 
    for(uint i=numOfBurns; i>=1; i--){ 
        if (burnTimestampArr[i-1] <thisWeekStartTime){ 
        	break;
        	}
        total += burnAmountArr[i-1]; 
    } 
    return total; 
} 
            
function getThisWeekBurnAmountLeft() public view returns(uint){ 
    return weeklyLimit - getThisWeekBurnedAmount(); 
} 

function burn(uint amount) external payable { 
    require(amount <= getThisWeekBurnAmountLeft()); 
    require(IERC20(tokenAddress).transferFrom(msg.sender, BURN_ADDRESS,amount)); 
    (numOfBurns = add_uint256(numOfBurns,1)); 
}

function getThisWeekBurnedAmount() public view returns( uint){ 
    uint thisWeekStartTime=getThisWeekStartTime(); Patching arithmetic Saner
     uint total = 0; 
    for(uint i = numOfBurns; i>=1 ;(i=sub_uint256(i, 1))){ 
        if (burnTimestampArr[sub_uint256(i,1)] < thisWeekStartTime) break; 
           total = add_uint256(total,burnAmountArr[ sub_uint256(i,1)]); 
        } 
    return total; 
 } 
           
function getThisWeekBurnAmountLeft() public view returns(uint){ 
    return sub_uint256(weeklyLimit, getThisWeekBurnedAmount()); 
} 
             
function burnPatched(uint amount) external payable nonReentrant{ 
    require(amount <= getThisWeekBurnAmountLeft()); 
    require(IERC20(tokenAddress).transferFrom(msg.sender, BURN_ADDRESS,amount)); 
    (numOfBurns = add_uint256(numOfBurns,1)); 
}
Security Code Recommendations for Smart Contract (Zhou et al.)  [3]

Illegal Coverage

- function getTags() external view returns(
bytes32) {
+ function getTags() external view returns(
bytes32 memory ) {
Reentrancy

- if(msg.sender.call.value(_am)()) { balances[
msg.sender] -= _am;
+ if(msg.sender.send(_am)) { balances[msg.
sender] -= _am;
Incorrect Inheritance Order

- function init(BaseWallet _wallet) public
virtual onlyWallet(_wallet) {
+ function init(BaseWallet _wallet) public
virtual override onlyWallet(_wallet) {
Authorization Through tx.origin

- require(tx.origin == owner);
+ require(msg.sender == owner);
Missing Return Statement

- function onTokenTransfer(address, uint,
bytes calldata) external ;
+ function onTokenTransfer(address, uint,
bytes calldata) external returns(bool);
Use of Deprecated Functions

- if (!approve(_spender, _amount)) throw;
+ if (!approve(_spender, _amount)) revert();
Erroneous Visibility

- function insert(uint256 storage heapList,
uint256 k) public {
+ function insert(uint256 storage heapList,
uint256 k) internal {
Unchecked Return Value

- hon1ninja.send(this.balance - 1 ether);
+ if (!hon1ninja.send(this.balance - 1 ether))
revert();
Arithmetic Issue

- balanceOf[to] += value;
+ require(balanceOf[to] >= value);
	balanceOf[to] += value; 
Erroneous Variable Type

- if(recipientImplementation != 0)
+ if(recipientImplementation != address(0))
Solidity Keyword Addition

- LogSetAuthority(authority);
+ emit LogSetAuthority(authority);
SafeMath Library Use

- return totalSupply - totalBorrow;
+ return totalSupply.sub(totalBorrow);
Tips: towards automating patch suggestion for vulnerable smart contracts (Chen et al.) [4]

Fixing unchecked external calls.

Inserting call checking:
address.external_calls (ethers);

+ if (!address.external_calls (ethers)) ( throw; )

Replacing the external call:
- address.external_calls(ethers);
+ address.transfer(ethers)
Fixing reentrancy.

**Replacing the reentrancy call:
**
- address.call.value (ethers)
+ address.send/transfer(ethers)

Moving the statement with state variables:
+ statements with state variables;

...msg.sender.call.value(ethers) ...

- statements with state variables;
Fixing access control.

Replacing the authenticating variable:

- tx.origin == Owner 
+ msg. sender == owner

Replacing the incorrect constructor:

- otherFuncName ()
+ constructor/contractName ()

Inserting the missing protection:

+ require (msg. sender == contractOwner) ;
Authority-sensitive statements
Fixing arithmetic issue.

Inserting the missing protection:

a = b + c;
+ require (a >= b ll a >= c);
OR
+ require (b >= c);
a = b - c;
OR
a = b * c;
+ require (c = a / b);
OR
a += bi
+ require (a >= b);
+ require (a >= b);
a -= bi
OR
+ uint tmp = a;
*= b；
require (b = a / tmp);
Fixing strict balance equality.

Replacing the authenticating variable:
this.balance == val
+ this. balance >= val &d this.balance < val + 1
Fixing unmatched type assignment.

Replacing the int type:
for(uint i - 0; i < val; i++)
+ for（int/uint256 i=0; i < val; i++)

Inserting a suicide function.

Inserting the missing interrupter:
+ function suicide () {
require (contractOwner = msg. sender);
selfdestruct (this.balance);
}
Fixing hard coded address.

function hardencode () {
address dest = Oxeeeeeeeeeeeeeeeeeeee;
+ function hardencode (address param) (
+address dest = param;
Smart Contract Code Repair Recommendation based on Reinforcement Learning  [5]

When the value exceeds this range, an overflow will occur. Therefore, after operations such as +, -, *, and /, this vulnerability arises when the variable is not validated in time for its value. This is an arithmetic.

By executing Approval method in line 14, a user A (i.e., msg.sender) allows a user B (i.e.,spender) to transfer N tokens by calling approval function. If A wants to change the allowed transfer amount from N to M, but B has already sent a transaction to transfer N and executed it first, then B can transfer N tokens before A modifies the transfer amount, resulting in A’s additional loss. One of the fix suggestions is to add a field to the inputs of approve, which is the expected current value and to have approved revert if B’s current allowance is not what A indicated she was expecting [65]. For example, a statement require(_allowed msg.sender==0||value==0); can be added before line 13.

contract TransactionOrderDependence {
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    mapping(address => uint256) private _balances;
    mapping(address => mapping(address => uint256)) private _allowed;
    uint256 private _totalSupply;

    constructor(uint totalSupply) {
        _balances[msg.sender] = totalSupply;
    }

    function approve(address spender, uint256 value) public returns (bool) {
        require(spender != address(0));
+        require(_allowed[msg.sender][spender] == 0 || value == 0);
        _allowed[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
        return true;
    }
}

### References

[1] Chen, J., Xia, X., Lo, D., Grundy, J., Luo, X., & Chen, T. (2020). Defining smart contract defects on ethereum. *IEEE Transactions on Software Engineering*, *48*(1), 327-345.

[2] Nguyen, T. D., Pham, L. H., & Sun, J. (2021, May). SGUARD: towards fixing vulnerable smart contracts automatically. In *2021 IEEE Symposium on Security and Privacy (SP)* (pp. 1215-1229). IEEE.

[3] Zhou, X., Chen, Y., Guo, H., Chen, X., & Huang, Y. (2023, March). Security Code Recommendations for Smart Contract. In *2023 IEEE International Conference on Software Analysis, Evolution and Reengineering (SANER)* (pp. 190-200). IEEE.

[4] Chen, Q., Zhou, T., Liu, K., Li, L., Ge, C., Liu, Z., ... & Bissyandé, T. F. (2023). Tips: towards automating patch suggestion for vulnerable smart contracts. *Automated Software Engineering*, *30*(2), 31.

[5] Guo, H., Chen, Y., Chen, X., Huang, Y., & Zheng, Z. (2024). Smart contract code repair recommendation based on reinforcement learning and multi-metric optimization. *ACM Transactions on Software Engineering and Methodology*, *33*(4), 1-31.

