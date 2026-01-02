from kivy.uix.accordion import BooleanProperty
from kivy.uix.accordion import NumericProperty
from kivy.app import App
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock


Builder.load_file('Gui/kv.kv')

class ColoredBox(GridLayout):
    def __init__(self, bg_color=(1,1,1,1), **kwargs):
        super().__init__(**kwargs)
        self.bg_color = bg_color
        with self.canvas.before:
            Color(*self.bg_color)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

class Task_listView(RecycleView):
    def __init__(self, data=None, **kwargs):    
        super().__init__(**kwargs)
        if data:
            self.data = [{"text": val} for val in data]

    def refresh_data_index(self):
        'Updates data Index when a element is deleted'
        
        for i, task in enumerate(self.data):
            task['index'] = i

class TaskCell(RecycleDataViewBehavior, BoxLayout):
    text = StringProperty("")
    index = NumericProperty(0)
    editing = BooleanProperty(False)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super().refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.is_double_tap:
                self.editing = True
                Clock.schedule_once(self.focus_input, 0)
                return True
        return super().on_touch_down(touch)

    def focus_input(self, dt):
        for child in self.children:
            if isinstance(child, TextInput):
                child.focus = True
                child.select_all()

    def save_text(self, new_text):
        self.text = new_text
        self.editing = False
        self.parent.parent.data[self.index]["text"] = new_text
# --- MainApp ---

class TaskManagerApp(App):
    def __init__(self, tasks:dict, **kwargs):
        super().__init__(**kwargs)
        self.tab_names = []  # Stores the names of all existing tabs
        self.tasks = tasks

    def build(self):
        """
        BoxLayout
            Tab_bar(BoxLayout)
            MainBox(gridLayout)
                ContentBox
                ButtonBox
                    add_taskButton
        """
        self.task_index = 0

        root = BoxLayout(orientation="vertical")
        self.tab_bar = BoxLayout(size_hint_y=None, height=40)
        self.MainBox = GridLayout(cols=1)
        self.ContentBox = ColoredBox(cols=1)
        self.ButtonBox = GridLayout(cols=3,
                                    size_hint_y=None,
                                    height=140,
                                    )
        self.ButtonBox.cols = 3
        self.manager = ScreenManager()

        self.Build_tasks()

        self.add_tabButton = Button(text="+", size_hint_x=None, width=120)
        self.add_tabButton.bind(on_press = lambda x: self.create_tab("New Tab"))
        self.tab_bar.add_widget(self.add_tabButton)

        self.add_taskButton = Button(text='Add Task',
                                    background_color=(0, 1, 0.8, 1),
                                    size_hint=(1, None),
                                    height=50,
                                    )
        self.add_taskButton.bind(on_release=lambda x: self.create_task('hola', self.manager.current))

        self.ButtonBox.add_widget(GridLayout())
        #Center Button
        centerDiv = GridLayout(cols=1)

        centerDiv.add_widget(BoxLayout())
        centerDiv.add_widget(self.add_taskButton)
        centerDiv.add_widget(BoxLayout())


        self.ButtonBox.add_widget(centerDiv)
        # --------------------------------------
        self.ButtonBox.add_widget(GridLayout())

        # Add Widgets
        root.add_widget(self.tab_bar)
        root.add_widget(self.MainBox)

        self.MainBox.add_widget(self.ContentBox)
        self.ContentBox.add_widget(self.manager)
        self.MainBox.add_widget(self.ButtonBox)

        return root
    
    def create_tab(self, title):
        "Set NewTab name = title, Creates Screen and adds tab to bar"

        new_title = self.create_title(title)

        # Create screen with "Empty" massage
        screen = Screen(name=new_title)
        screen.add_widget(Label(text='Empty', color='black'))
        self.manager.add_widget(screen)

        # Create tab button
        btn = Button(text=new_title, size_hint_x=None, width=120)
        btn.bind(on_release=lambda x: self.change_tab(new_title))

        # Insert before "+" button
        self.tab_bar.add_widget(btn, index=len(self.tab_bar.children))

        # Immediately show the new tab
        self.manager.current = new_title

    def create_task(self, task, pageName):
        screen = self.manager.get_screen(pageName)

        if type(screen.children[0]) == type(Task_listView()):   # If there is Task_listView in page
            task_list = screen.children[0]    # Get Task_listView OBJ
        else: # If screen has label
            screen.remove_widget(screen.children[0])    # If there is not Task_listView in page
            task_list = Task_listView()     # Create OBJ
            screen.add_widget(task_list)

        task_list.data.append({'text' : task})
        
    def delete_task(self, index):
        screen = self.manager.get_screen(self.manager.current)
        task_list = screen.children[0] # Get task_list obj

        task_list.data.pop(index)

        task_list.refresh_data_index()

    def change_tab(self, name):
        self.manager.current = name

    def create_title(self, title):
        if title in self.tab_names:
            number = 1
            while True:     # Adds one number per every time is title used in self.tab_names
                test_title = title + f'({number})'
                number += 1
                if test_title not in self.tab_names:
                    title = test_title
                    break
        
        self.tab_names.append(title)
        
        return title
    
    def Build_tasks(self):
        "Reads Task From Json File and create structure in App"
        # Create tabs
        tabs = self.tasks[1:]
        for tab in tabs:
            self.create_tab(tab['PageName'])
            # Create List View

            for task in tab['PageTasks']:
                self.create_task(task, tab['PageName'])