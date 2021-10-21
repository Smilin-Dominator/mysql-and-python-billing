import io


class bill(object):

    def __init__(self, stream: io.TextIOWrapper):
        self.file = stream
        self.lines = self.file.read().splitlines()

    def grand_total(self) -> str:
        grand_total = " ".join([e for e in self.lines if e.startswith('**Grand Total:')])
        return grand_total.strip("**Grand Total: <span style='color:yellow'>").strip("</span>**<br>")[3:]

    def name(self) -> str:
        name = " ".join([e for e in self.lines if e.startswith('**Customer')])
        return name.strip('**Customer: <span style="color:green">').strip('</span>**<br>')
