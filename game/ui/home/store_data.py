import json,os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from dataclasses import dataclass
from typing import Optional

from pygame import Surface
from game.assets import shield_item,plasma_item,precision_item,nural_item,research_item,toxins_item

@dataclass
class NeuralComponent:
    id:str
    name:str
    description:str
    type: str
    rarity:str
    level_required:int
    effects:list[str]
    unlock_condition:str
    bought:bool
    status:dict[str,int]
    price:int
    image:Optional[Surface] = None


    @staticmethod
    def from_dict(data:dict) -> 'NeuralComponent':
        return NeuralComponent(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            type=data["type"],
            rarity=data["rarity"],
            level_required=data["level_required"],
            effects=data.get("effects", []),
            unlock_condition=data["unlock_condition"],
            bought=data["bought"],
            status=data.get("stats", {}),
            price=data["price"]
        )




@dataclass
class ListNueralModel:
    listItem: list[NeuralComponent]

    @staticmethod
    def from_list(data: list[dict]) -> 'ListNueralModel':
        return ListNueralModel(
            listItem=[NeuralComponent.from_dict(item) for item in data]
        )


class StoreData:
    def __init__(self):
        self.base_path = os.path.dirname(__file__)  

    def getCategoryItem(self, category: str, isBought: bool) -> ListNueralModel:
        file_path = os.path.join(self.base_path, "storage", f"{category}.json")
        
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                data = ListNueralModel.from_list(data)
                images = self.item(category)
                print(len(data.listItem))
                for i, value in enumerate(images):
                    data.listItem[i].image = value
                data.listItem = [item for item in data.listItem if item.bought == isBought]
                return data

        except Exception as e:
            import traceback
            traceback.print_exc()
            return None

    @staticmethod
    def item(category:str)->list[Surface]:
            if category=="nural" or category =="":
                return nural_item
            elif category=="plasma":
                return plasma_item
            elif category=="precision":
                return precision_item
            elif category=="shield":
                return shield_item
            elif category=="research":
              
                return research_item
            elif category=="toxin":
                return toxins_item        
       
    def bought(self, category: str, index: int):
        file_path = os.path.join(self.base_path, "storage", f"{category}.json")
        try:
            with open(file_path, 'r+') as file:
                data = json.load(file)
                data[index]["bought"] = True
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()
        except (FileNotFoundError, KeyError, IndexError, TypeError) as e:
            print(f"Error accessing data: {e}")
            return None
            
