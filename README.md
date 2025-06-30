# Supersim End-to-End Test

This guide describes how to run a manual L2-to-L2 message relay test using the `GasTank` and `MessageSender` contracts. Inspired by [this](https://supersim.pages.dev/guides/interop/cast#cast-commands-to-relay-interop-messages) guide.

## Prerequisites

- `foundry`, `go`, and `supersim` must be installed.
- A local `supersim` instance must be running. Start it with the following command:

  ```bash
  supersim
  ```

## Setup and Execution Steps

### 1. Deploy Contracts

Deploy the GasTank and MessageSender contracts to both chains:

```bash
# Deploy contracts to supersim chains 901 and 902
forge script script/sol/SetupSupersim.s.sol:SetupSupersim --broadcast
```

### 2. Run the Test Scripts

Navigate to the scripts directory and run the tests:

```bash
cd script/go

# Run token relay test between L2 chains
go run . relay

# Run GasTank relay test with nested cross-chain messages
go run . gastank --numNestedMessages 5

# Run gas usage analysis across different message counts
go run . gasanalysis
```
