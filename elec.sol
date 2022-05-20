pragma solidity 0.4.24;

contract Election {
    struct Candidate {
        uint id;
        string name;
        uint voteCount;
    }
    
    bool public chalu = true;
    mapping(uint => Candidate) public candidates;
    uint public candidatesCount;
    string public temp;
    
    event votedEvent (
        uint indexed _candidateid
    );
    
    constructor () public {
        addCandidate ("Candidate 1");
        addCandidate ("Candidate 2");
        
    }
    
    function end () public {
        chalu = false;
    }
    function addCandidate (string memory _name) private {
        candidatesCount ++;
        candidates[candidatesCount] = Candidate(candidatesCount , _name, 0);
        
    }
    function display (uint _candidateid) view public returns (uint){
        return candidates[_candidateid].voteCount;
        
    }
    
    function disname(uint _candidateid) public returns (string memory){
        temp= candidates[_candidateid].name;
        return temp;
    }
    
    function vote (uint _candidateid) public {
        require(chalu, "Election Ended");
        
        candidates[_candidateid].voteCount ++;
        emit votedEvent (_candidateid);
    }
    
    
}
