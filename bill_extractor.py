class bill(object):

    def __init__(self, stream):
        self.file = stream
        self.lines = self.file.read().splitlines()

    def date(self) -> str:
        # **Date: <span style="color:blue">21/10/2021</span>**<br>
        pass

    def time(self) -> str:
        # **Time: <span style="color:red">09.42 PM</span>**<br>
        pass

    def customer(self) -> str:
        # **Customer: <span style="color:green">Barney Stinson</span>**<br>
        name = self.lines[6]
        name = name[:-13]
        return name[38:]

    def grand_total(self) -> str:
        # **Grand Total: <span style='color:yellow'>Rs. 12200</span>**<br>
        grand_total = " ".join([e for e in self.lines if e.startswith('**Grand Total:')])
        return grand_total.strip("**Grand Total: <span style='color:yellow'>").strip("</span>**<br>")[3:]

    def transferred(self) -> bool or None:
        # **Transferred Cash: <span style="color:magenta">False</span>**<br>
        t_line = self.lines[-1]
        if self.lines[-1].startswith("**Transferred"):
            t_line = t_line[48:]
            t_line = t_line[:-13]
            print(t_line)
            if t_line == "True":
                return True
            else:
                return False
        else:
            return None
