import json

# Open and read JSON file

class data_json:
    def __str__(self):
        return f'data = {str(self.sort_jsonData())}'

    def __init__(self):
        """JSON structure:
        'name' : 'UserName',
        'tasks' : 
            {
                PageName : []
            }
        """
        with open('data.json', 'r+', encoding='utf-8') as file:
            try:
                self.data = json.load(file)
            except json.decoder.JSONDecodeError: # Json File Empty
                # Add empty data to Json
                self.data = json.dumps({
                                "name" : "UserName",
                                "tasks" : {
                                        'New Tab': [
                                            'lavar loza',
                                            'barrer la casa',
                                            'Preparar la comida',
                                            'Hacer la cama'
                                        ]
                                    }
                            }, sort_keys=True, indent=4)
                file.write(self.data)

    def sort_jsonData(self):
        """Returns : [UserName, [{PageName :['task1', 'task2'....]}, ....]]
            Each element after [0] is a DICT of each page
        """
        sorted_data = [self.data["name"]]

        # Splits Tasks pages
        for task in self.data['tasks']:
            sorted_data.append({task : self.data['tasks'][task]})

        return sorted_data
    
    def create_page(self, PageName:str):
        self.data['tasks'][PageName] = []

    def create_task(self, PageName, Task):
        self.data['tasks'][PageName].append(Task)

    def delete_task(self, PageName, Task):
        try:
            self.data['tasks'][PageName].remove(Task)
        except ValueError:
            pass

    def write(self):
        'Write changes in JSON file'
        with open('data.json', 'w', encoding='utf-8') as file:  # Open JSON file
            json.dump(self.data, file, ensure_ascii=False, indent=4)    # Save changes in JSON

json_OBJ = data_json()