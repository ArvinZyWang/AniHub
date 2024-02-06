# No GUI version
import utils.scraper as scraper
import utils.update_manager as um
from utils.menu_in_terminal import Menu
from prettytable import PrettyTable
import pyperclip

# 主菜单
# 查询订阅
def subscription():
    def subscription_management():
        subscription_data = um.load_subscription()
        table = PrettyTable()
        table.field_names = ['No.','Title']
        for index, anime in enumerate(subscription_data):
            table.add_row([index+1, anime['title']])
        print(table)
        subscription_management_operations = {'增加订阅': add_subscription, '移除订阅': remove_subscription}
        subscription_management_menu = Menu('订阅管理', subscription_management_operations, parent=subscription_menu)
        subscription_management_menu.display_menu()
        
    subscription_actions = {'更新订阅': check_update, '未看更新': unwatched, '订阅管理': subscription_management}
    subscription_menu = Menu('订阅', subscription_actions, parent=main_menu)
    subscription_menu.display_menu()
    
# 搜索番剧
def search():
    str = input("请输入查询关键词，顺序为：[番剧名称] [分类(可选)] [发布组(可选)] [排序方式(可选)]\n")
    args = str.split(' ')
    print('正在搜索中, 请稍候...')
    result = scraper.search(*args)
    page = 0
    
    def next_page():
        nonlocal page
        page += 1
    def prev_page():
        nonlocal page
        page -= 1
        
    search_menu_choices = {'上一页': prev_page, '下一页': next_page, '打印磁力链': lambda: print_search_result_magnet(result)}
    search_menu = Menu('搜索选项', search_menu_choices, parent= main_menu)
    while True:
        print_search_result(result, page)
        search_menu.display_menu()


choices_main = {'订阅': subscription, '搜索': search}
main_menu = Menu('主菜单', choices_main)

# 订阅菜单
def check_update():
    um.check_update()
    subscription()

def unwatched():
    subscription_data = um.load_subscription()
            
    # 打印存在更新的番剧名称和数量
    table = PrettyTable()
    table.field_names = ['No.','Title','Number of New']
    for index, anime in enumerate(subscription_data):
        if anime['New'] != []:
            table.add_row([index, anime['title'], len(anime['New'])])
    print(table)
    anime_index = int(input("请输入想查看的番剧序号："))
    
    def print_new_magnet():
        num = int(input("请输入序号：")) -1
        print(subscription_data[anime_index]['New'][num]['magnet'])
        pyperclip.copy(subscription_data[anime_index]['New'][num]['magnet'])
        print('已写入剪切板')
        subscription_unwatched_menu.display_menu()
    
    def marked_as_watched():
        num = int(input("请输入序号：")) - 1
        um.marked_as_watched(anime_index, num)
        subscription_unwatched_menu.display_menu()

    print_new(subscription_data[anime_index]['New'])
    subscription_unwatched = {'打印磁力链':print_new_magnet, '标记为看过':marked_as_watched, '返回上一级':unwatched, '返回主菜单': main_menu.display_menu}
    subscription_unwatched_menu = Menu('订阅操作', subscription_unwatched)
    subscription_unwatched_menu.display_menu()

  
def add_subscription():
    str = input("请输入新订阅的信息，顺序为：[番剧名称] [发布组(可选)]\n")
    args = str.split(' ')
    um.subscribe(*args)
    print(f'番剧{args[0]}已添加到订阅列表中')
    subscription()

def remove_subscription():
    subscription_data = um.load_subscription()
    table = PrettyTable()
    table.field_names = ['No.','Title']
    for index, anime in enumerate(subscription_data):
        table.add_row([index+1, anime['title']])
    print(table)
    remove_index = int(input('请输入要移除的序号：')) -1
    try:
        confirm = input(f"要移除的番剧为： {subscription_data[remove_index]['title']} 是否确认? Y/N ").upper().strip()
        if confirm == 'Y':
            subscription_data.pop(remove_index)
            um.update_subscription(subscription_data)
            subscription()
        else:
            subscription()
    except IndexError:
        print('没有这个序号')
        remove_subscription()
    except ValueError:
        print('请输入数字')
        remove_subscription()
    
  
def print_new(list_of_new):
    table = PrettyTable()
    table.field_names = ['No.', 'Title', 'Pub Date']
    for index in range(len(list_of_new)):
        if index < len(list_of_new):
            dict = list_of_new[index]
            table.add_row([index+1, dict['title'], dict['pubDate']])
        else:
            break
    print(table)
    
        

# 搜索菜单
def print_search_result(result:list[dict], page, items_each_page = 10):
    selected_pages = range(page*items_each_page, (page+1)*items_each_page)
    table = PrettyTable()
    table.field_names = ['No.', 'Title', 'Pub Date']
    for index in selected_pages:
        if index < len(result):
            dict = result[index]
            table.add_row([index+1, dict['title'], dict['pubDate']])
        else:
            break
    print(table)
    total_pages = (len(result) + items_each_page -1 ) // items_each_page
    print(f'第{page + 1}页，共{total_pages}页')

def print_search_result_magnet(result):
    num = int(input('请输入序号：')) -1
    print(result[num]['magnet'])
    pyperclip.copy(result[num]['magnet'])
    print('已写入剪切板')
    subchoice = input('是否返回上一级? Y/N ').upper().strip()
    if subchoice == 'Y':
        main_menu.display_menu()
    


if __name__ == '__main__':
    main_menu.display_menu()
