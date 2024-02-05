class Menu:
    """
    {
        'choice1': func1,
        'choice2': func2
    }
    """
    def __init__(self, name:str, choices_funcs:dict, parent:'Menu' = None) -> None:
        self.name = name
        self.choices_funcs = choices_funcs
        self.parent = parent
        if not self.parent is None:
            self.choices_funcs['返回上一级'] = parent.display_menu
        return
    
    def show_choice(self):
        print('='*20, self.name, '='*20)
        for index,key in enumerate(self.choices_funcs):
            print('-', index+1,' ', key)
            
    def ask_choice(self):
        keys = list(self.choices_funcs.keys())
        try:
            choice = int(input('请输入选项：')) - 1
            self.choices_funcs[keys[choice]]()
        except IndexError:
            print('无该选项, 请重新输入')
            self.ask_choice()
        except ValueError:
            print('请输入数字')
            self.ask_choice()
        return
            
    def display_menu(self):
        self.show_choice()
        self.ask_choice()
        
        
            
    
if __name__ =='__main__':
    def func1():
        print('func1 was called.')
        
    def func2():
        print('func2 was called.')
        
    t1 = {
        'choice1': func1,
        'choice2': func2,
    }
    
    test_menu = Menu('test', t1)
    test_menu.display_menu()
    
    test_submenu = Menu('submenu', t1, parent=test_menu)
    test_submenu.display_menu()