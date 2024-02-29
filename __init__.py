from loader import load
from UI.app import App
from taskmanager import TaskManager
import asyncio

async def main():

    load()

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