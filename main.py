from Gui.gui import TaskManagerApp

# Run tasks offline
import offline_mode


# Run App
if __name__ == '__main__':
    task_OBJ = offline_mode.json_OBJ
    TaskManagerApp(task_OBJ).run()