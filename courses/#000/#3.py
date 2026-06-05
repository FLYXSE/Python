class Scanner:
    def scan(self, document):
        print(f"Сканирование документа: {document}")


class Printer:
    def print(self, document):
        print(f"Печать документа: {document}")


class Fax:
    def send_fax(self, document, number):
        print(f"Отправка факса документа '{document}' на номер {number}")


class MultiFunctionDevice(Scanner, Printer, Fax):
    def copy(self, document):
        self.scan(document)
        self.print(document)
