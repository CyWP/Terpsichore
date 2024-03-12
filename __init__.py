from loader import load
from UI.app import App
from taskmanager import TaskManager
from appstate import AppState
from os import path
import asyncio

async def main():

    load()

    app = App()

    TaskManager.register_task(asyncio.create_task(app.mainloop()))

    AppState.set_app(app)
    AppState.set_root(path.join(path.expanduser('~'), 'Documents', 'Terpsichore_Data'))
    AppState.load(path.abspath('DATA/state.json'))

    try:
        await asyncio.gather(TaskManager.run_tasks())
    except KeyboardInterrupt:
        pass
    finally:
        await TaskManager.cancel_tasks()

if __name__ == "__main__":
    asyncio.run(main())