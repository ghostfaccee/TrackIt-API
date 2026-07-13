import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_stats_api(client: AsyncClient, auth: str):
    habit_create = await client.post('/v1/habit/create', json = {'name' : 'Habit', 'description' : ''}, headers = {'Authorization' : f'Bearer {auth}'})
    habit_id = habit_create.json()['id']
    await client.post(f'/v1/log/{habit_id}', json = {'completed' : True}, headers = {'Authorization' : f'Bearer {auth}'})
    response = await client.get(f'/v1/stats/{habit_id}', headers = {'Authorization' : f'Bearer {auth}'})
    assert response.json()['total_days'] == 1
    assert response.json()['streak'] == 1

@pytest.mark.asyncio
async def test_get_stats_habit_not_found_api(client: AsyncClient, auth: str):
    response = await client.get('/v1/stats/999', headers = {'Authorization' : f'Bearer {auth}'})
    assert response.status_code == 404
