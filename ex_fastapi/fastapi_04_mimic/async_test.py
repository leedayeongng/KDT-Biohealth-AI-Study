import asyncio
import time

#비동기 함수
async def test_trans(item_id, text):
    print(f"시작 항목:{item_id}:{text} 번역..")
    #비동기 함수의 처리를 기다림
    await asyncio.sleep(1)
    result = f'{text} 번역됨'
    print(f'완료 항목:{item_id}:{result}')
    return result

async def main():
    items = ["heart", "blood", "lung", "brain"]
    st_time = time.time()
    # 1.동기 방식(순차처리)
    print('\n-- 1.순차적처리--------')
    for i,item in enumerate(items):
        await test_trans(i+1, item)
    end_time = time.time() - st_time
    print(f'순차 처리 총 : {end_time:.2f}초')

    #2.비동기(병렬처리)
    st_time = time.time()
    # 여러 테스크 동시 실행
    tasks = [test_trans(i+1, item) for i, item in enumerate(items)]
    results= await asyncio.gather(*tasks) # 여러비동기함수를 동시실행
    end_time = time.time() - st_time
    print(f'비둘기 처리중:{end_time:.2f}초')
if __name__ == '__main__':
    asyncio.run(main())


