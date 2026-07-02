import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_habit_api(client: AsyncClient):
    response = await client.post('/v1/habit/create', json = {'name' : 'Habit', 'description' : 'Description'})
    assert response.status_code == 201
    data = response.json()
    assert data['name'] == 'Habit'
    assert data['description'] == 'Description'
    assert 'id' in data

@pytest.mark.asyncio
async def test_get_all_habits_api(client: AsyncClient):
    for _ in range(3):
        await client.post('/v1/habit/create', json = {'name' : 'Habit', 'description' : 'Description'})
    response = await client.get('/v1/habits')
    data = response.json()
    assert len(data) == 3

@pytest.mark.asyncio
async def test_get_habit_by_id_api(client: AsyncClient):
    create = await client.post('/v1/habit/create', json = {'name' : 'Habit', 'description' : ''})
    habit_id = create.json()['id']
    response = await client.get(f'/v1/habit/{habit_id}')
    data = response.json()
    assert data['name'] == create.json()['name']

@pytest.mark.asyncio
async def test_delete_habit_by_id_api(client: AsyncClient):
    create = await client.post('/v1/habit/create', json = {'name' : 'Habit', 'description' : ''})
    habit_id = create.json()['id']
    response = await client.delete(f'/v1/habit/{habit_id}')
    assert response.status_code == 204

@pytest.mark.asyncio
async def test_update_habit_by_id_api(client: AsyncClient):
    create = await client.post('/v1/habit/create', json = {'name' : 'Habit', 'description' : ''})
    habit_id = create.json()['id']
    response = await client.put(f'/v1/habit/{habit_id}', json = {'name' : 'New name', 'description' : 'New description'})
    assert response.json()['name'] != create.json()['name']
    assert response.json()['description'] != create.json()['description']

@pytest.mark.asyncio
async def test_habit_not_found_api(client: AsyncClient):
    response = await client.get('/v1/habit/999')
    assert response.status_code == 404
