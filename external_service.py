import asyncio
from typing import Literal
from httpx import AsyncClient



async def make_request(
    url: str,
    base_url: str,
    method: Literal['GET', 'POST', 'PUT', 'DELETE'] = 'GET',
    data: dict = None,

) -> dict:
    attempts = 3
    attempt = 0

    url = f'{base_url}{url}'

    while True:
        try:
            async with AsyncClient(timeout=120) as session:
                response = await session.request(method, url, json=data)
                content = response.json()
                return {
                    'status': response.status_code,
                    'headers': dict(response.headers),
                    'body': content,
                }
        except Exception as e:
            print(e)
            attempt += 1
            await asyncio.sleep(1)
            if attempt == attempts:
                return {
                    'status': 500,
                    'headers': {},
                    'body': {},
                }