from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleview import RecycleView
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

KV = '''
<EditableItem>:
    orientation: "horizontal"

    Label:
        text: root.text
        opacity: 0 if root.editing else 1

    TextInput:
        text: root.text
        opacity: 1 if root.editing else 0
        multiline: False
        on_text_validate: root.save_text(self.text)

<MyTaskList>:
    id: rv
    viewclass: "EditableItem"
    RecycleBoxLayout:
        default_size: None, dp(40)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: "vertical"

<RV>:
    viewclass: 'Label'
    RecycleBoxLayout:
        default_size: None, dp(48)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
'''

class EditableItem(RecycleDataViewBehavior, BoxLayout):
    text = StringProperty("")
    editing = BooleanProperty(False)
    index = None

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

class MyTaskList(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = [
            {'text': f'Item {i}'} for i in range(1, 11)
        ]

class AddTaskView(App):
    def build(self):
        Builder.load_string(KV)
        return MyTaskList()

if __name__ == '__main__':
    AddTaskView().run()
