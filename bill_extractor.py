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


class bill(object):

    def __init__(self, stream):
        self.file = stream
        self.lines = self.file.read().splitlines()

    def date(self) -> str:
        # **Date: <span style="color:blue">21/10/2021</span>**<br>
        date = self.lines[4]
        return date[33:-13]

    def time(self) -> str:
        # **Time: <span style="color:red">09.42 PM</span>**<br>
        time = self.lines[5]
        return time[32:-13]

    def customer(self) -> str:
        # **Customer: <span style="color:green">Barney Stinson</span>**<br>
        name = self.lines[6]
        return name[38:-13]

    def grand_total(self) -> str:
        # **Grand Total: <span style='color:yellow'>Rs. 12200</span>**<br>
        grand_total = " ".join([e for e in self.lines if e.startswith('**Grand Total:')])
        return grand_total[42:-13]

    def transferred(self) -> bool or None:
        # **Transferred Cash: <span style="color:magenta">False</span>**<br>
        t_line = self.lines[-1]
        if self.lines[-1].startswith("**Transferred"):
            t_line = t_line[48:-13]
            if t_line == "True":
                return True
            else:
                return False
        else:
            return None
