from fastapi import APIRouter, Request
from core import YumeApp

from helpers.msgpack import read_request, respond
from models import *

router = APIRouter()

# Chinese (EN translate WIP)
# 当我们以新账户登录游戏时，玩家的游戏等级达到10级时，点击"公演"按钮，
# 游戏将触发进入匹配房间列表的指引，在不进行patch的情况下，
# 直接点击游戏所指的 roomlist 按钮，会直接触发错误(errcode:81),
# 因此我们将"/api/MultiRooms"接口返回空列表，
# 取代上游multi_room.py文件(49-54)原返回的[MultiRoomInformationResult()]列表，
# 从而避免游戏报错。
# Device-tested.

# /api/MultiRooms
@router.get("/api/MultiRooms")
async def multi_room_get_multi_rooms(request: Request):
    return respond([])

# /api/MultiRooms/Joined
@router.post("/api/MultiRooms/Joined")
async def multi_room_get_joined_multi_rooms(request: Request):
    return respond([])

# /api/MultiRooms/Invited
@router.post("/api/MultiRooms/Invited")
async def multi_room_get_invited_multi_rooms(request: Request):
    return respond([])

# Not Tested:

# # /api/MultiRooms/Create
# @router.post("/api/MultiRooms/Create")
# async def multi_room_create_multi_rooms(request: Request):
#     app: YumeApp = request.app
#     payload = await read_request(request, CreateMultiRoomPayload)
#     return respond(MultiRoomCreateResult())


# # /api/MultiRooms/Detail?hashedMultiRoomId=?hashedMultiRoomId=
# @router.post("/api/MultiRooms/Detail?hashedMultiRoomId=")
# async def multi_room_get_multi_room_detail(
#     request: Request, hashedMultiRoomId: Optional[str] = None
# ):
#     app: YumeApp = request.app
#     payload = {}  # no payload
#     return respond(MultiRoomDetailResult())



# # /api/MultiRoom/GetSearchMultiRooms?HashedRoomId=&LiveMasterId=
# @router.get("/api/MultiRoom/GetSearchMultiRooms")
# async def multi_room_get_search_multi_rooms(
#     request: Request,
#     HashedRoomId: Optional[str] = None,
#     LiveMasterId: Optional[int] = None,
# ):
#     app: YumeApp = request.app
#     payload = {}  # no payload
#     return respond([])


# # /api/MultiRooms/Join
# @router.post("/api/MultiRooms/Join")
# async def multi_room_join_multi_rooms(request: Request):
#     app: YumeApp = request.app
#     payload = await read_request(request, JoinMultiRoomPayload)
#     return respond(BooleanResult())


# # /api/MultiRooms/Release?hashedMultiRoomId=?hashedMultiRoomId=
# @router.post("/api/MultiRooms/Release?hashedMultiRoomId=")
# async def multi_room_release_multi_rooms(
#     request: Request, hashedMultiRoomId: Optional[str] = None
# ):
#     app: YumeApp = request.app
#     payload = {}  # no payload
#     return respond(BooleanResult())


# # /api/MultiRooms/Resignation?hashedMultiRoomId=?hashedMultiRoomId=
# @router.post("/api/MultiRooms/Resignation?hashedMultiRoomId=")
# async def multi_room_resignation_multi_room(
#     request: Request, hashedMultiRoomId: Optional[str] = None
# ):
#     app: YumeApp = request.app
#     payload = {}  # no payload
#     return respond(BooleanResult())


# # /api/MultiRooms/Send/Invite
# @router.post("/api/MultiRooms/Send/Invite")
# async def multi_room_send_multi_room_invite(request: Request):
#     app: YumeApp = request.app
#     payload = await read_request(request, InviteMultiRoomPayload)
#     return respond(BooleanResult())


def install(app):
    """Place these compatibility handlers before upstream placeholder routes."""
    app.router.routes[0:0] = list(router.routes)