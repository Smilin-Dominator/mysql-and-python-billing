class bill(object):

    def __init__(self, stream: io.TextIOWrapper):
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
        grand_total = " ".join([e for e in self.lines if e.startswith('**Grand Total:')])
        return grand_total.strip("**Grand Total: <span style='color:yellow'>").strip("</span>**<br>")[3:]

    def name(self) -> str:
        name = " ".join([e for e in self.lines if e.startswith('**Customer')])
        return name.strip('**Customer: <span style="color:green">').strip('</span>**<br>')
