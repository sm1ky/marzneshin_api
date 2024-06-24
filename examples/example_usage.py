import asyncio
from marzneshin.api import MarzneshinAPI
from marzneshin.models import UserCreate, UserModify
from datetime import datetime

async def main():
    base_url = 'http://127.0.0.1:3500'
    username = 'admin'
    password = 'admin'

    api = MarzneshinAPI(base_url, username, password)

    # Получение списка пользователей
    users = await api.get_users()
    print("Users:", users)

    # Добавление нового пользователя
    new_user_data = UserCreate(
        username='newuser',
        data_limit=1073741824,  # 1GB
        enabled=True,
        status='active',
        services=[1, 2]
    )
    new_user = await api.add_user(new_user_data)
    print("New User:", new_user)

    # Получение информации о пользователе
    user_info = await api.get_user('newuser')
    print("User Info:", user_info)

    # Изменение данных пользователя
    modified_user_data = UserModify(
        username='newuser',
        services=[
            2
        ]
    )
    modified_user = await api.modify_user('newuser', modified_user_data)
    print("Modified User:", modified_user)
    
    user_info = await api.get_user('newuser')
    print("User Info:", user_info)

    # Удаление пользователя
    await api.remove_user('newuser')
    print("User removed")

if __name__ == '__main__':
    asyncio.run(main())