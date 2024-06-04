from pythonosc import osc_server
from pythonosc.dispatcher import Dispatcher
import asyncio
from appstate import AppState 
from taskmanager import (
    TaskManager,
)
from ENGINE.engine import Engine 


class OSCControlServer:

    _listener = None
    _stop = False

    @classmethod
    def start(cls):
        TaskManager.register_task(asyncio.create_task(cls.start_server()))

    @classmethod
    async def start_server(cls):

        async def loop():
            while not cls._stop:
                await asyncio.sleep(0.1)

        def launch():
            TaskManager.register_task(asyncio.create_task(Engine.launch()))

        def abort():
            AppState.abort_engine()

        ip = "127.0.0.1"
        port = AppState.get_attr("listen_port")
        dispatcher = Dispatcher()
        dispatcher.map("/start", launch)
        dispatcher.map("/stop", abort)

        server = osc_server.AsyncIOOSCUDPServer(
            (ip, port), dispatcher, asyncio.get_event_loop()
        )
        transport, protocol = await server.create_serve_endpoint()

        try:
            await loop()
        finally:
            transport.close()

    @classmethod
    def stop(cls):
        AppState.abort_engine()
        cls._stop = True
