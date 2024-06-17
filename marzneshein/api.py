import aiohttp
from typing import Optional, List, Any, Dict
from .models import AdminCreate, AdminModify, NodeCreate, NodeModify, ServiceCreate, ServiceModify, InboundHost, UserCreate, UserModify

class MarznesheinAPI:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.token = None
        self.headers = {
            'Content-Type': 'application/json',
            'accept': 'application/json'
        }

    async def _get_token(self):
        async with aiohttp.ClientSession() as session:
            session.headers['Content-Type'] = 'application/x-www-form-urlencoded'
            async with session.post(f'{self.base_url}/api/admins/token', data={
                'username': self.username,
                'password': self.password
            }) as response:
                data = await response.json()
                self.token = data['access_token']
                self.headers['Authorization'] = f'Bearer {self.token}'

    async def _request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None):
        if not self.token:
            await self._get_token()

        url = f'{self.base_url}{endpoint}'

        if data is not None:
            data = {k: v for k, v in data.items() if v is not None}

        if params is not None:
            params = {k: v for k, v in params.items() if v is not None}

        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.request(method, url, json=data, params=params) as response:
                response.raise_for_status()
                return await response.json()

    # Admin Methods
    async def get_admins(self, username: Optional[str] = None, page: int = 1, size: int = 50):
        params = {'username': username, 'page': page, 'size': size}
        return await self._request('GET', '/api/admins', params=params)

    async def create_admin(self, admin: AdminCreate):
        return await self._request('POST', '/api/admins', data=admin.model_dump(exclude_unset=True))

    async def get_current_admin(self):
        return await self._request('GET', '/api/admins/current')

    async def modify_admin(self, username: str, admin: AdminModify):
        return await self._request('PUT', f'/api/admins/{username}', data=admin.model_dump(exclude_unset=True))

    async def remove_admin(self, username: str):
        return await self._request('DELETE', f'/api/admins/{username}')

    # Node Methods
    async def get_nodes(self, status: Optional[List[str]] = None, name: Optional[str] = None, page: int = 1, size: int = 50):
        params = {'status': status, 'name': name, 'page': page, 'size': size}
        return await self._request('GET', '/api/nodes', params=params)

    async def add_node(self, node: NodeCreate):
        return await self._request('POST', '/api/nodes', data=node.model_dump(exclude_unset=True))

    async def get_node(self, node_id: int):
        return await self._request('GET', f'/api/nodes/{node_id}')

    async def modify_node(self, node_id: int, node: NodeModify):
        return await self._request('PUT', f'/api/nodes/{node_id}', data=node.model_dump(exclude_unset=True))

    async def remove_node(self, node_id: int):
        return await self._request('DELETE', f'/api/nodes/{node_id}')

    async def reconnect_node(self, node_id: int):
        return await self._request('POST', f'/api/nodes/{node_id}/resync')

    async def get_node_xray_config(self, node_id: int):
        return await self._request('GET', f'/api/nodes/{node_id}/xray_config')

    async def alter_node_xray_config(self, node_id: int, data: dict[str, Any]):
        return await self._request('PUT', f'/api/nodes/{node_id}/xray_config', data=data)

    async def get_node_settings(self):
        return await self._request('GET', '/api/nodes/settings')

    async def get_node_usage(self, start: Optional[str] = None, end: Optional[str] = None):
        params = {'start': start, 'end': end}
        return await self._request('GET', '/api/nodes/usage', params=params)

    # Service Methods
    async def get_services(self, name: Optional[str] = None, page: int = 1, size: int = 50):
        params = {'name': name, 'page': page, 'size': size}
        return await self._request('GET', '/api/services', params=params)

    async def add_service(self, service: ServiceCreate):
        return await self._request('POST', '/api/services', data=service.model_dump(exclude_unset=True))

    async def get_service(self, service_id: int):
        return await self._request('GET', f'/api/services/{service_id}')

    async def modify_service(self, service_id: int, service: ServiceModify):
        return await self._request('PUT', f'/api/services/{service_id}', data=service.model_dump(exclude_unset=True))

    async def remove_service(self, service_id: int):
        return await self._request('DELETE', f'/api/services/{service_id}')

    # Inbound Methods
    async def get_inbounds(self, tag: Optional[str] = None, page: int = 1, size: int = 50):
        params = {'tag': tag, 'page': page, 'size': size}
        return await self._request('GET', '/api/inbounds', params=params)

    async def get_inbound(self, inbound_id: int):
        return await self._request('GET', f'/api/inbounds/{inbound_id}')

    async def get_inbound_hosts(self, inbound_id: int, page: int = 1, size: int = 50):
        params = {'page': page, 'size': size}
        return await self._request('GET', f'/api/inbounds/{inbound_id}/hosts', params=params)

    async def create_inbound_host(self, inbound_id: int, host: InboundHost):
        return await self._request('POST', f'/api/inbounds/{inbound_id}/hosts', data=host.model_dump(exclude_unset=True))

    async def update_inbound_host(self, host_id: int, host: InboundHost):
        return await self._request('PUT', f'/api/inbounds/hosts/{host_id}', data=host.model_dump(exclude_unset=True))

    async def delete_inbound_host(self, host_id: int):
        return await self._request('DELETE', f'/api/inbounds/hosts/{host_id}')

    async def get_hosts(self, page: int = 1, size: int = 50):
        params = {'page': page, 'size': size}
        return await self._request('GET', '/api/inbounds/hosts', params=params)

    # User Methods
    async def get_users(self, username: Optional[str] = None, status: Optional[List[str]] = None, 
                        order_by: Optional[str] = None, descending: bool = False, page: int = 1, size: int = 50):
        params = {
            'username': username, 'status': status, 'order_by': order_by,
            'descending': str(descending).lower(), 'page': page, 'size': size
        }
        return await self._request('GET', '/api/users', params=params)

    async def add_user(self, user: UserCreate):
        return await self._request('POST', '/api/users', data=user.model_dump(exclude_unset=True))

    async def get_user(self, username: str):
        return await self._request('GET', f'/api/users/{username}')

    async def modify_user(self, username: str, user: UserModify):
        return await self._request('PUT', f'/api/users/{username}', data=user.model_dump(exclude_unset=True))

    async def remove_user(self, username: str):
        return await self._request('DELETE', f'/api/users/{username}')

    async def reset_user_data_usage(self, username: str):
        return await self._request('POST', f'/api/users/{username}/reset')

    async def enable_user(self, username: str):
        return await self._request('POST', f'/api/users/{username}/enable')

    async def disable_user(self, username: str):
        return await self._request('POST', f'/api/users/{username}/disable')

    async def revoke_user_subscription(self, username: str):
        return await self._request('POST', f'/api/users/{username}/revoke_sub')

    async def get_user_usage(self, username: str, start: Optional[str] = None, end: Optional[str] = None):
        params = {'start': start, 'end': end}
        return await self._request('GET', f'/api/users/{username}/usage', params=params)

    async def set_owner(self, username: str, admin_username: str):
        params = {'admin_username': admin_username}
        return await self._request('PUT', f'/api/users/{username}/set-owner', params=params)

    # Subscription Methods
    async def user_subscription(self, username: str, key: str):
        return await self._request('GET', f'/sub/{username}/{key}')

    async def user_subscription_info(self, username: str, key: str):
        return await self._request('GET', f'/sub/{username}/{key}/info')

    async def user_get_usage(self, username: str, key: str, start: Optional[str] = None, end: Optional[str] = None):
        params = {'start': start, 'end': end}
        return await self._request('GET', f'/sub/{username}/{key}/usage', params=params)

    async def user_subscription_with_client_type(self, username: str, key: str, client_type: str):
        return await self._request('GET', f'/sub/{username}/{key}/{client_type}')

    # System Stats Methods
    async def get_admins_stats(self):
        return await self._request('GET', '/api/system/stats/admins')

    async def get_nodes_stats(self):
        return await self._request('GET', '/api/system/stats/nodes')

    async def get_users_stats(self):
        return await self._request('GET', '/api/system/stats/users')