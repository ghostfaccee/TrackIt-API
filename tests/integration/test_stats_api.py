import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_stats_api(client: AsyncClient):
    habit_create = await client.post('/v1/habit/create', json = {'name' : 'Habit', 'description' : ''})
    habit_id = habit_create.json()['id']
    await client.post(f'/v1/log/{habit_id}', json = {'completed' : True})
    response = await client.get(f'/v1/stats/{habit_id}')
    assert response.json()['total_days'] == 1
    assert response.json()['streak'] == 1

@pytest.mark.asyncio
async def test_get_stats_habit_not_found_api(client: AsyncClient):
    response = await client.get('/v1/stats/999')
    assert response.status_code == 404
