import asyncio
from .vpn import VPN
from fastapi import APIRouter
from starlette.responses import JSONResponse
from .socks import SocksServer
router = APIRouter()

vpn = VPN()

socks = None

def send_response(success):
    return JSONResponse(status_code=200 if success else 501, content={'status': "up" if success else "down"})

@router.get('/status', summary="Get Status of the VPN", description="Get Status of the VPN")
async def go(
):

    return send_response(success=vpn.is_active)

@router.get('/activate', summary="Activate the VPN", description="Activate the VPN")
async def activate(
):

    global socks

    success = await vpn.start()

    if success:
        loop = asyncio.get_running_loop()
        if socks is None:
            socks = loop.create_server(SocksServer, '0.0.0.0', 8081)
            asyncio.create_task(socks)

    return send_response(success=success)

