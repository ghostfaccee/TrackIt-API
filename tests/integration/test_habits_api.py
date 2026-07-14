import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_habit_api(client: AsyncClient, auth: str):
    response = await client.post('/v1/habit/create', json = {'name' : 'Habit', 'description' : 'Description'}, headers = {'Authorization' : f'Bearer {auth}'})
    assert response.status_code == 201
    data = response.json()
    assert data['name'] == 'Habit'
    assert data['description'] == 'Description'
    assert 'id' in data

@pytest.mark.asyncio
async def test_get_all_habits_api(client: AsyncClient, auth: str):
    for _ in range(3):
        await client.post('/v1/habit/create', json = {'name' : 'Habit', 'description' : 'Description'}, headers = {'Authorization' : f'Bearer {auth}'})
    response = await client.get('/v1/habits', headers = {'Authorization' : f'Bearer {auth}'})
    data = response.json()
    assert len(data) == 3

@pytest.mark.asyncio
async def test_get_habit_by_id_api(client: AsyncClient, auth: str):
    create = await client.post('/v1/habit/create', json = {'name' : 'Habit', 'description' : ''}, headers = {'Authorization' : f'Bearer {auth}'})
    habit_id = create.json()['id']
    response = await client.get(f'/v1/habit/{habit_id}', headers = {'Authorization' : f'Bearer {auth}'})
    data = response.json()
    assert data['name'] == create.json()['name']

@pytest.mark.asyncio
async def test_delete_habit_by_id_api(client: AsyncClient, auth: str):
    create = await client.post('/v1/habit/create', json = {'name' : 'Habit', 'description' : ''}, headers = {'Authorization' : f'Bearer {auth}'})
    habit_id = create.json()['id']
    response = await client.delete(f'/v1/habit/{habit_id}', headers = {'Authorization' : f'Bearer {auth}'})
    assert response.status_code == 204

@pytest.mark.asyncio
async def test_update_habit_by_id_api(client: AsyncClient, auth: str):
    create = await client.post('/v1/habit/create', json = {'name' : 'Habit', 'description' : ''}, headers = {'Authorization' : f'Bearer {auth}'})
    habit_id = create.json()['id']
    response = await client.put(f'/v1/habit/{habit_id}', json = {'name' : 'New name', 'description' : 'New description'}, headers = {'Authorization' : f'Bearer {auth}'})
    assert response.json()['name'] != create.json()['name']
    assert response.json()['description'] != create.json()['description']

@pytest.mark.asyncio
async def test_habit_not_found_api(client: AsyncClient, auth: str):
    response = await client.get('/v1/habit/999', headers = {'Authorization' : f'Bearer {auth}'})
    assert response.status_code == 404
