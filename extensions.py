import requests

tok = "2111825011:AAHC1bH2uLi1Pn1Mmc2WHLaIAjkvk5-3z6w" #токин бота
url = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5" # адресс API ПриватБанка, оттуда бирем данные по валюте
RULES = """Бот обмена валют DS2021Bot(DreamSweat).\n 1. Создан для отображения курсов валют Долара, Евро, Рубля
на основе стоимости украинской гривне(values эта команда отображает валюты). Можна это сделать с помощью клавиши Курс Валют
или ввода с клавиатуры
Курс Валют.\n 2. Калькулятор валюты. Пользователь вводит через пробел сокращение валюты (USD -долар, EUR - евро ,
RUR - рубль, UAH - гривня ) и сумму что надо перевести. Пример USD EUR 100 - переcчитает сколько евро стоит 100 доларов. 
Также есть инлайн клавиатура, с зарание выщитанными значениями."""

#Классы исключений
class CurrencyError(Exception):
    pass
class CurrencyErrorExept(CurrencyError):
    def __str__(self):
        return "Такой валюты нету в списке"
class CurrencyErrorFail(CurrencyError):
    def __str__(self):
        return "Не верно указаны параметри ввода, введите данные согласно правил. Ознакомится с правилами /help"

#Класс Валюта. Принемает в себя валюту для рассчета стоимости
class Currency():
    Key_C = ["RUR", "USD", "EUR"]
    Key_Chek = ["RUR", "USD", "EUR", "UAH"]

    def __init__(self, cur_out = "USD" , cur_in = "EUR", value = 100 ):
        self.cur_in = cur_in
        self.cur_out = cur_out
        self.value = value

    def __str__(self):
        if self.cur_in in Currency.Key_Chek and self.cur_out in Currency.Key_Chek and isinstance(self.value, int) or isinstance(self.value, float):
            return f"Производится рассчет едениц {self.value} {self.cur_out} в {self.cur_in}, стоимость {self.answer:.2f} "
        else:
            raise CurrencyErrorExept

    #метод рассчета курса одной валюты в другую
    @property
    def answer(self):
        res = requests.get(url).json()
        if self.cur_out in Currency.Key_C:
            for _ in res:
                if self.cur_out in _["ccy"]:
                    sale = _["sale"]
        elif self.cur_out == "UAH":
            sale = 1
        if self.cur_in in Currency.Key_C:
            for _ in res:
                if self.cur_in in _["ccy"]:
                    sale2 = _["sale"]
        elif self.cur_in == "UAH":
                sale = 1
        result = self.value*float(sale)/float(sale2)
        return result


