from pydantic import BaseModel


class HashFileRow(BaseModel):
    filepath:   str
    hash:       str


class Doll(BaseModel):
    Name: str
    Price: int
    Quantity: int = None
    Total: int = None
    old_quantity: int = None
    old_total: int = None

    def set_old_quantity(self):
        self.old_total = self.Total
        self.old_quantity = self.Quantity

    def to_tuple(self) -> tuple[str | int, ...]:
        return tuple([self.Name, self.Price, self.Quantity, self.Total])