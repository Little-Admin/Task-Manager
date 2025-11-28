tab_names = ['']

def create_title(title):
        if title in tab_names:
            number = 1
            while True:     # Adds one number per every time is title used in self.tab_names
                test_title = title + f'({number})'
                number += 1
                if test_title not in tab_names:
                    title = test_title
                    break
        
        tab_names.append(title)

        return title

name1 = create_title('New Tab')
name2 = create_title('New Tab')
name3 = create_title('New Tab')

print(name1, name2, name3)