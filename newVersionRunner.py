import asyncio
from newVersionConnector import EthClient


async def main():
    # Websocket Messages
    BLOCK_SUBSCRIBE_MSG = {"id": 1, "method": "eth_subscribe", "params": ["newHeads"]}

    # Connection
    eth_node1_client = EthClient("ETH_HOST:10001")
    
    await eth_node1_client.open(BLOCK_SUBSCRIBE_MSG)

asyncio.run(main())
