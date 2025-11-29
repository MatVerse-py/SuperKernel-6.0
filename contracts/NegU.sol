// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

interface IEntropyOracle {
    function readOmega() external view returns (uint256);
}

/// @title NegU – Neguentropy-backed ERC20
/// @notice Mints on entropy gain and burns on entropy loss, linking supply to Ω-score.
contract NegU {
    string public constant name = "NegU";
    string public constant symbol = "NEG";
    uint8 public constant decimals = 18;

    uint256 public totalSupply;
    address public immutable omegaOracle;
    uint256 public lastOmega;
    uint256 public constant THRESH = 0.85e18; // 0.85 with 18 decimals

    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Mint(address indexed to, uint256 value, uint256 omega);
    event Burn(address indexed from, uint256 value, uint256 omega);

    constructor(address _oracle) {
        omegaOracle = _oracle;
        lastOmega = IEntropyOracle(_oracle).readOmega();
    }

    function _updateOmega(address actor) internal {
        uint256 omega = IEntropyOracle(omegaOracle).readOmega();
        if (omega > lastOmega && omega > THRESH) {
            uint256 negToMint = (omega - lastOmega) * 1e12; // scale entropy delta
            _mint(actor, negToMint);
        } else if (omega < lastOmega) {
            uint256 negToBurn = (lastOmega - omega) * 1e12;
            _burn(actor, negToBurn);
        }
        lastOmega = omega;
    }

    function transfer(address to, uint256 amount) external returns (bool) {
        _updateOmega(msg.sender);
        _transfer(msg.sender, to, amount);
        return true;
    }

    function approve(address spender, uint256 amount) external returns (bool) {
        allowance[msg.sender][spender] = amount;
        emit Transfer(msg.sender, spender, 0);
        return true;
    }

    function transferFrom(address from, address to, uint256 amount) external returns (bool) {
        _updateOmega(from);
        allowance[from][msg.sender] -= amount;
        _transfer(from, to, amount);
        return true;
    }

    function _transfer(address from, address to, uint256 amount) internal {
        balanceOf[from] -= amount;
        balanceOf[to] += amount;
        emit Transfer(from, to, amount);
    }

    function _mint(address to, uint256 amount) internal {
        totalSupply += amount;
        balanceOf[to] += amount;
        emit Transfer(address(0), to, amount);
        emit Mint(to, amount, lastOmega);
    }

    function _burn(address from, uint256 amount) internal {
        balanceOf[from] -= amount;
        totalSupply -= amount;
        emit Transfer(from, address(0), amount);
        emit Burn(from, amount, lastOmega);
    }
}
