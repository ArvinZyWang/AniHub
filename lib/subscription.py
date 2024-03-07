import json
from models.team import teams
from models.subscribed_anime import SubscribedAnime

class Subscription:
    
    data:list[SubscribedAnime] = None
    
    def __init__(self):
        self.load()
        
    def load(self):
        try:
            with open(r'./data/subscribed.json', 'r', encoding='utf-8') as f:
                self.data = [SubscribedAnime.new(self, item) for item in json.load(f)]
                self.data.sort(key = lambda anime: anime.NewCount, reverse = True)
                self.save(copy = True)
                if not self.data:
                    self.data = []
        except json.JSONDecodeError as e:
            self.data = []
        except FileNotFoundError as e:
            self.data = []
        except Exception as e:
            print(f'Unable to load subscription, error: {e}')
    
    def save(self, copy = False):
        if copy:
            self.data.sort(key = lambda anime: anime.NewCount, reverse = True)
            with open(r'./data/subscribed_copy.json','w', encoding='utf-8') as f:
                json.dump([item.to_dict() for item in self.data], f, indent = 4)
        else:
            with open(r'./data/subscribed.json','w', encoding='utf-8') as f:
                json.dump([item.to_dict() for item in self.data], f, indent = 4)
            
    def add(self, title:str, team:str):
        teams[team]
        if title in [item.title for item in self.data]:
            raise Exception(f'{title} is already subscribed.')
        anime = SubscribedAnime(self, {'title': title, 'team': team})
        self.data.append(anime)
        self.save()
        
    def remove(self, arg:str|int):
        if type(arg) == str:
            title_list = [item.title for item in self.data]
            if arg in title_list:
                index = title_list.index(arg)
                self.__removeByIndex(index)
            else:
                raise Exception(f'Remove Error: {arg} not exist.')
        elif type(arg) == int:
            self.__removeByIndex(arg)
    
    def __removeByIndex(self, index:int):
        removed = self.data.pop(index)
        print(f'{removed.title}@{removed.team} is removed from subscription.')
        self.save()
    
    def __repr__(self) -> str:
        return f"Dataclass for subscription data."
    
if __name__ == '__main__':
    subscription = Subscription()
    example = subscription.data[0]
    breakpoint()