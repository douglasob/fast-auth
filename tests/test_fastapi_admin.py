import pytest
from fast_auth import __version__
from fast_auth.auth.auth import create_user_cli
from fast_auth.migration import create_auth_tables, drop_auth_tables
from httpx import AsyncClient

from .server_test import app


def test_version():
    assert __version__ == '0.1.0'


@pytest.mark.asyncio
async def test_initial_migration():
    await drop_auth_tables()
    await create_auth_tables()


def test_create_user():
    create_user_cli()


@pytest.mark.asyncio
async def test_authenticate():
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post('/login', json={'username': 'douglas', 'password': '123'})
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_session_db():
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get('/test_session_db')
        assert response.status_code == 200
        print(response.json())


@pytest.mark.asyncio
async def test_check_token_jwt():
    async with AsyncClient(app=app, base_url='http://test') as client:
        token = await client.post(url='login', json={'username': 'douglas', 'password': '123'})
        token = token.json()

        response = await client.get('authenticated', headers={'Authorization': f'Bearer {token["access"]}'})
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_error_token_jwt():
    async with AsyncClient(app=app, base_url='http://test') as client:
        token = await client.post(url='login', json={'username': 'douglas', 'password': '123'})
        token = token.json()

        response = await client.get('authenticated')
        assert response.status_code == 401
