// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.7.0 <0.8.0;
pragma experimental ABIEncoderV2;

/**
 * @title SpectralCommandRelay
 */ 
    
/*
	SpectralCommandRelay (SCR) acts as a messaging service designed for use as a command relay for operatives
	
	Utilizes a One -> Many messaging model where commanders/shepherds send a message to whichever tags/channels they wish to communicate with
	
	Recommendations:
	    Perform encryption before sending message, decrypt on receiving end. End-to-end is the responsibility of the commander.
	
	Needed Upgrades:
	    Generation of PostHash needs more randomization (and removal of speakcount), currently leaks info on posting amount / speak count
	    Add in ability to remove my own messages (can't actually remove but can cut them from being processed)

    Recepient Features:
        Designed to support E2E Encryption of commands and data
        Designed to support fully customizable recipents and opcodes
        Recepients "call home" to an anonymous Web3_Endpoint & Smart_Contract, using arbitrary paramaters
        Recepients are designed with persistence features
*/

contract SpectralCommandRelay {
    
    // Basic Information
    string hello_str = "SpectralCommandRelay (SCR): msg service, broadcasts to tags, recommend encrypt msg before posting";
    string burn_str = "Blacklists sender, use if compromised";
    
    // Burnt Addresses are unable to interact.
    // Burning must be self-initiated.
    // Burning acts as a failsafe in case your keys are compromised
    // Collection of burnt address
    mapping(address => bool) BurntLedger;
    
    struct User {
        address uid;
        uint256 speakcount;
    }
    
    // Collection of user speak count, used in hashing
    mapping(address => uint256) SpeakCount;
    
    
    /*
        Using an address, one may view a users number of posts and post hashes
        Using a hash, one may view the post
    */
    // Collection of all Posts, indexed by PostHash
    mapping(bytes32 => string) Posts;
    
    struct PostHashes {
        bytes32[] Hashes;
    }
    
    /*
        #Taging
        A post can contain #tags that entities can search for
    */
    mapping(bytes32 => PostHashes) AddressedTaggedPostHashes; // hash(address+tag) => PostHashes
    mapping(bytes32 => uint256) AddressedTaggedPostCount; // hash(address+tag) => Post Count
    
    /*
        Basic Functions
    */
    // Explains what this is
    function info() public view returns (string memory){
        require(BurntLedger[msg.sender] == false);
        
        return hello_str;
    }

    // Explains what burn does
    function info_burn() public view returns (string memory){
        require(BurntLedger[msg.sender] == false);
        
        return burn_str;
    }
    
    // Get the contract address
    function info_contract_address() public view returns (address){
        require(BurntLedger[msg.sender] == false);
        
        return address(this);
    }
    
    /*
        Account Functions
    */
    // Will burn sender account rendering it unusable
    function burn() public {
        require(BurntLedger[msg.sender] == false);
        
        BurntLedger[msg.sender] = true;
    }
    
    /*
        Posting
    */
    // Post function (full)
    function push_post(string calldata _message, string[] calldata _tags) public {
        require(BurntLedger[msg.sender] == false);
        
        // Derive hash of msg.sender + index
        bytes32 _hash = keccak256(abi.encodePacked(msg.sender, SpeakCount[msg.sender] + 1)); //TODO Should upgrade this to have some randomness, leaks info about postcount

        // Post
        Posts[_hash] = _message;

        // Add PostHash to senders collection seperated by tags
        for (uint i = 0; i < _tags.length; i++){
            // Derive hash of address + tag
            bytes32 _hash_add_tag = keccak256(abi.encodePacked(msg.sender, _tags[i]));
            
            AddressedTaggedPostHashes[_hash_add_tag].Hashes.push(_hash);
            AddressedTaggedPostCount[_hash_add_tag] = AddressedTaggedPostCount[_hash_add_tag] + 1;
        }

        //Inc Sender Speak Count
        SpeakCount[msg.sender] = SpeakCount[msg.sender] + 1;
    }
    
    /*
        Read a Post
    */
    // Get post from posthash
    function get_post(bytes32 _posthash) public view returns (string memory){
        require(BurntLedger[msg.sender] == false);
        
        return Posts[_posthash];
    }
    
    /*
        Get collections of Posts from user & tag
    */
    function get_postcount_from_address_tag(address _poster, string calldata _tag) public view returns (uint256){
        require(BurntLedger[msg.sender] == false);
        
        // Derive hash of address + tag
        bytes32 _hash = keccak256(abi.encodePacked(_poster, _tag));
        
        return AddressedTaggedPostCount[_hash];
    }
    
    function get_posthashes_from_address_tag(address _poster, string calldata _tag) public view returns (bytes32[] memory){
        require(BurntLedger[msg.sender] == false);
        
        // Derive hash of address + tag
        bytes32 _hash = keccak256(abi.encodePacked(_poster, _tag));
        
        return AddressedTaggedPostHashes[_hash].Hashes;
    }
    
    function get_posthash_from_address_tag_id(address _poster, string calldata _tag, uint256 _id) public view returns (bytes32){
        require(BurntLedger[msg.sender] == false);
        
        // Derive hash of address + tag
        bytes32 _hash = keccak256(abi.encodePacked(_poster, _tag));
        
        return AddressedTaggedPostHashes[_hash].Hashes[_id - 1]; //Minus 1 because we treat posts as count not index. ie. "_id" will be index+1. It's weird I know.
    }
}