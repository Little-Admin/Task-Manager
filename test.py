class taksview:
    def __init__(self):
        self.data = [
            {"text":"hola", "index": 0},
            {"text":"hola 1", "index": 1},
            {"text":"hola 2", "index": 2}
        ]

    def del_row(self, index):
        self.data.pop(index)

    def update_index(self):
        for i, val in enumerate(self.data):
            print(val, i)

a = taksview()
a.del_row(1)
a.update_index()