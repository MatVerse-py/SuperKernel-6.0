// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

contract OracleMock {
    uint256 private omega = 0.9e18;

    function setOmega(uint256 value) external {
        omega = value;
    }

    function readOmega() external view returns (uint256) {
        return omega;
    }
}
