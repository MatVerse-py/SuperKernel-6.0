const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying with", deployer.address);

  const OracleMock = await hre.ethers.getContractFactory("OracleMock");
  const oracle = await OracleMock.deploy();
  await oracle.waitForDeployment();

  const NegU = await hre.ethers.getContractFactory("NegU");
  const negu = await NegU.deploy(await oracle.getAddress());
  await negu.waitForDeployment();

  const CaptalsPrimeChain = await hre.ethers.getContractFactory("CaptalsPrimeChain");
  const chain = await CaptalsPrimeChain.deploy();
  await chain.waitForDeployment();

  console.log("Oracle:", await oracle.getAddress());
  console.log("NegU:", await negu.getAddress());
  console.log("Prime Chain:", await chain.getAddress());
}

// Simple mock just to satisfy NegU dependency during local dev
async function deployMocks() {}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
