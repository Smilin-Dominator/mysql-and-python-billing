"""
MySQL And Python Billing
Copyright (C) 2021 Devisha Padmaperuma

MySQL And Python Billing is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

MySQL And Python Billing is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with MySQL And Python Billing.  If not, see <https://www.gnu.org/licenses/>.
"""

from pydantic import BaseModel


class HashFileRow(BaseModel):
    filepath:       str = None
    filehash:       str = None
    filecontents:   str = None


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