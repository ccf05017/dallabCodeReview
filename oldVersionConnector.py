from websockets import connect
import asyncio
import json

async def main():

    try:
        eth_websocket = await connect("ws://ETH_HOST:10001")
        try:
            await eth_websocket.send(json.dumps({"id": 1, "method": "eth_subscribe", "params": ["newHeads"]}))
            while True:
                new_block_sub_response = await asyncio.wait_for(eth_websocket.recv(), timeout=60)
                print(new_block_sub_response)
                # 실제 서비스에는 이후 로직이 좀 더 있어서 코드가 훨씬 지저분합니다
                # 또한 지금 코드처럼 주르르륵 짜 놓은 형태이기 때문에 가독성이 최악 수준입니다.
                # ETH_HOST에 getTransactionCountByHash 질의를 통한 block 별 transaction 수 확인
                # transaction 수가 1 이상이면? -> ETH_HOST에 각 transaction receipt 정보 제공
    
        except Exception as e2:
            # newblock 이벤트 구독 시도, 메시지 수신 실패 시 재시도를 해야 하는데!
            print(e2)
    
        finally:
            if eth_websocket != None:
                eth_websocket.close()
    
    except Exception as e1:
        # websocket 연결 자체가 끊길 때도 재시도를 해야 하는데!
        print(e1)
    
    finally:
        if eth_websocket != None:
            eth_websocket.close()

asyncio.run(main())