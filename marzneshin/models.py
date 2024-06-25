from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

# Admin Models
class Admin(BaseModel):
    username: str
    is_sudo: bool

class AdminCreate(BaseModel):
    username: str
    is_sudo: bool
    password: str

class AdminModify(BaseModel):
    password: str
    is_sudo: bool

# Node Models
class NodeBase(BaseModel):
    name: str
    address: str
    port: Optional[int] = 53042
    connection_backend: Optional[str] = "grpclib"
    usage_coefficient: Optional[float] = 1.0

class NodeCreate(NodeBase):
    inbounds: Optional[List[int]] = []

class NodeModify(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    port: Optional[int] = None
    connection_backend: Optional[str] = None
    usage_coefficient: Optional[float] = None
    inbounds: Optional[List[int]] = None
    status: Optional[str] = None

# Service Models
class ServiceBase(BaseModel):
    name: str
    users: Optional[List[int]] = []
    inbounds: Optional[List[int]] = []

class ServiceCreate(ServiceBase):
    pass

class ServiceModify(BaseModel):
    name: Optional[str] = None
    inbounds: Optional[List[int]] = None

# Inbound Models
class InboundHost(BaseModel):
    remark: str
    address: str
    port: Optional[int] = None
    sni: Optional[str] = None
    host: Optional[str] = None
    path: Optional[str] = None
    security: Optional[str] = "inbound_default"
    alpn: Optional[str] = ""
    fingerprint: Optional[str] = ""
    allowinsecure: Optional[bool] = None
    is_disabled: Optional[bool] = None
    mux: Optional[bool] = False
    fragment: Optional[Dict[str, str]] = None

# User Models
class UserCreate(BaseModel):
    username: str
    expire: Optional[datetime] = None
    data_limit: Optional[int] = 0
    data_limit_reset_strategy: Optional[str] = "no_reset"
    enabled: Optional[bool] = True
    status: Optional[str] = 'active'
    service_ids: Optional[List[int]] = []
    note: Optional[str] = None
    on_hold_expire_duration: Optional[int] = 0
    on_hold_timeout: Optional[datetime] = None

class UserModify(BaseModel):
    username: str
    expire: Optional[datetime] = None
    data_limit: Optional[int] = 0
    data_limit_reset_strategy: Optional[str] = "no_reset"
    enabled: Optional[bool] = True
    status: Optional[str] = 'active'
    service_ids: Optional[List[int]] = []
    note: Optional[str] = None
    on_hold_expire_duration: Optional[int] = 0
    on_hold_timeout: Optional[datetime] = None

# Subscription Models
class Subscription(BaseModel):
    username: str
    key: str

class SubscriptionUsage(BaseModel):
    username: str
    key: str
    start: Optional[str] = None
    end: Optional[str] = None

# Example Models
class ExampleResponse(BaseModel):
    message: str

# Validation Error Models
class HTTPValidationError(BaseModel):
    detail: List[str]

class ValidationError(BaseModel):
    loc: List[str]
    msg: str
    type: str