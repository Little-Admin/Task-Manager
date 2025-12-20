from Gui.gui import TaskManagerApp

# Run tasks offline
import offline_mode


# Run App
if __name__ == '__main__':
    tasks = offline_mode.json_OBJ.sort_jsonData()
    TaskManagerApp(tasks).run()