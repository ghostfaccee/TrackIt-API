import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_log_create_by_id_api(client: AsyncClient):
    habit_create = await client.post('/v1/habit/create', json = {'name' : 'Habit', 'description' : ''})
    habit_id = habit_create.json()['id']
    log_create = await client.post(f'/v1/log/{habit_id}', json = {'completed' : True})
    assert log_create.json()['id'] == 1
    assert log_create.json()['completed'] == True

@pytest.mark.asyncio
async def test_log_delete_by_id(client: AsyncClient):
    habit_create = await client.post('/v1/habit/create', json = {'name' : 'Habit', 'description' : ''})
    habit_id = habit_create.json()['id']
    log_create = await client.post(f'/v1/log/{habit_id}', json = {'completed' : True})
    log_id = log_create.json()['id']
    delete = await client.delete(f'/v1/log/{log_id}')
    assert delete.status_code == 204

@pytest.mark.asyncio
async def test_log_not_found_api(client: AsyncClient):
    log_delete = await client.delete('/v1/log/999')
    assert log_delete.status_code == 404