from kivy.core.window import Window
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder

# --- Colored BoxLayout (background color) ---
class ColoredBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(217/255, 217/255, 217/255, 1)   # RGBA
            self.bg = Rectangle(pos=self.pos, size=self.size)

        self.bind(size=self._update_bg, pos=self._update_bg)

    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size


# --- Main App ---
class TaskManagerApp(App):
    """
    root
        tab_bar
        BackgroundBox(FLoatLayout)
            contentBox
                ScreenManager()
                
            ButtonBox
    """
    def build(self):
        root = BoxLayout(orientation = 'vertical')

        # Tab bar (horizontal list of tabs)
        self.tab_bar = BoxLayout(size_hint_y=None, height=40)

        # Main Container
        BackgroundBox = FloatLayout()
        contentBox = ColoredBox(orientation='vertical',
                            size_hint=(0.9, 0.6),
                            pos_hint={'center_x': 0.5, 'center_y' : 0.7})


        # Window for switching content
        self.manager = ScreenManager()

        # Add first tab
        self.create_tab("New Tab", "None")

        # Assemble UI
        root.add_widget(self.tab_bar)
        BackgroundBox.add_widget(contentBox)
        contentBox.add_widget(self.manager)

        # Add "+" button
        self.add_tabButton = Button(text="+", size_hint_x=None, width=120)
        self.add_tabButton.bind(on_release=lambda x: self.create_tab("New Tab", "None"))
        self.tab_bar.add_widget(self.add_tabButton)

        root.add_widget(BackgroundBox)

        # Buttons
        ButtonBox = ColoredBox(orientation = "horizontal", size_hint=(.5, .2))

        addTaskButton = Button(text = "Add Task",
                               size_hint = (0.1, 0.1),
                               pos_hint = {'center_x': 0.5, 'center_y' : 0.5})

        BackgroundBox.add_widget(ButtonBox)
        ButtonBox.add_widget(addTaskButton)

        return root
        

    def create_tab(self, title, text):
        # Create screen
        screen = Screen(name=title)
        screen.add_widget(Label(text=text))
        self.manager.add_widget(screen)

        # Create tab button
        btn = Button(text=title, size_hint_x=None, width=120)
        btn.bind(on_release=lambda x: self.change_tab(title))

        # Insert before "+" button
        self.tab_bar.add_widget(btn, index=len(self.tab_bar.children))

        # Immediately show the new tab
        self.manager.current = title

    def change_tab(self, name):
        self.manager.current = name


# --- Run the App ---
if __name__ == "__main__":
    TaskManagerApp().run()
