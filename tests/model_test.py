from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class Item (BaseModel):
    name: str
    id: int

    def change_name(self, name: str) -> None:
        """Change the name of item"""
        self.name = name


example_item = Item(name="botox", id=0)

example_item.change_name("detox")

print( example_item.name )

