from loader import load
from UI.app import App
from taskmanager import TaskManager
from appstate import AppState
from os import path
import asyncio

async def main():

    load()

    AppState.load_state(path.abspath('DATA/ui_state.json'))

    app = App()

    TaskManager.register_task(asyncio.create_task(app.mainloop()))

    try:
        await asyncio.gather(TaskManager.run_tasks())
    except KeyboardInterrupt:
        pass
    finally:
        await TaskManager.cancel_tasks()

if __name__ == "__main__":
    asyncio.run(main())