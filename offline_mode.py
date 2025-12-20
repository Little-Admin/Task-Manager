import json

# Open and read JSON file

class data_json:
    def __init__(self):
        with open('data.json', 'r+', encoding='utf-8') as file:
            try:
                self.data = json.load(file)
            except json.decoder.JSONDecodeError: # Json File Empty
                # Add empty data to Json
                self.data = json.dumps({
                                "name" : "UserName",
                                "tasks" : [
                                    {
                                        'PageName' : 'New Tab',
                                        'PageTasks' : [
                                            'lavar loza',
                                            'barrer la casa',
                                            'Preparar la comida',
                                            'Hacer la cama'
                                        ]
                                    }
                                ]
                            }, sort_keys=True, indent=4)
                file.write(self.data)
            finally:
                file.close()

    def sort_jsonData(self):
        """Returns : [UserName, {PageName : 'Page1', PageTasks: ['task1', 'task2'....]}]
            Each element after [0] is a DICT of each page
        """
        sorted_data = [self.data["name"]]

        # Splits Tasks pages
        for task in self.data['tasks']:
            sorted_data.append(task)

        return sorted_data
    
json_OBJ = data_json()