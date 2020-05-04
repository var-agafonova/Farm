import random
import math

class animal_const: #константы для подсчета изменения поголовья животных
    BIRTH_ADULT = 0.7
    BIRTH_OLD = 0.4
    SURVIVAL_YOUNG = 0.9
    DEATH_OLD = 0.3
    ANIMAL_FEED = 100 #необходимый корм взрослому животному на год
    OLD = 2
    ADULT = 1
    YOUNG = 0
    

class Animals: 

    def __init__(self, numbers_of_animals, ava_feed): 
        #количество животных на ферме
        self.number = numbers_of_animals
        #корм необходимый для всех животных фермы
        self.nec_feed = math.ceil(animal_const.ANIMAL_FEED*(numbers_of_animals[animal_const.YOUNG]//2 + numbers_of_animals[animal_const.ADULT] + numbers_of_animals[animal_const.OLD]//3))
        #доступный корм на ферме
        self.ava_feed = ava_feed 
 
    def adverse_conditions(self): # умирание от неблагоприятных условий
        x = random.randint(5, 20)
        for i in [animal_const.YOUNG,animal_const.ADULT,animal_const.OLD]:
            self.number[i] = self.number[i]*(100-x)/100
 
    def feeding(self): # кормление и умирание от нехватки корма
        self.ava_feed -= self.nec_feed
        if self.ava_feed < 0:
            lack = 1-(self.ava_feed/self.nec_feed)
            for i in [animal_const.YOUNG,animal_const.ADULT,animal_const.OLD]:
                self.number[i] *= lack
                self.number[i] = math.ceil(self.number[i])
            self.ava_feed = 0
            #пересчет необходимого корма для животных
            self.nec_feed = math.ceil(animal_const.ANIMAL_FEED*(self.number[animal_const.YOUNG]//2 + self.number[animal_const.ADULT] + self.number[animal_const.OLD]//3))
    
    def livestock_growth(self): # рост поголовья
        self.number[animal_const.YOUNG] = math.ceil(animal_const.BIRTH_ADULT*self.number[1] + animal_const.BIRTH_OLD*self.number[2])
        self.number[animal_const.ADULT] = math.ceil(animal_const.SURVIVAL_YOUNG*self.number[0])
        self.number[animal_const.OLD] = math.ceil(self.number[1] + (1-animal_const.DEATH_OLD)*self.number[2])
        self.nec_feed = math.ceil(animal_const.ANIMAL_FEED*(self.number[0]//2 + self.number[1] + self.number[2]//3))

    def print_details(self):
        details = "\nКоличество животных на ферме:"
        details += ' '.join(map(str, self.number))
        details += "\nКорм в наличии: " + str(math.ceil(self.ava_feed))
        return details
    
class Contract:
    def __init__(self, remaining_period_r = 0, feed_number_r = 0, feed_price_r = 0, sold_animals_number_r = [0,0,0], sold_animals_price_r = [0,0,0], forfeit_r = 0):
        self.remaining_period = remaining_period_r
        self.sold_animals_number = sold_animals_number_r
        self.sold_animals_price = sold_animals_price_r
        self.forfeit = forfeit_r # неустойка
        self.feed_price = feed_price_r
        self.feed_number = feed_number_r
    
    def update(self): #ежегодное обновление данных онтракта
        self.remaining_period -= 1
        for i in [animal_const.YOUNG,animal_const.ADULT,animal_const.OLD]: #рост стоимости животных
            self.sold_animals_price[i] *= 1.1
            self.sold_animals_price[i] = math.ceil(self.sold_animals_price[i])

    def print_details(self):
        details = "\nОставшийся период контракта:"
        details += str(self.remaining_period)
        details += "\nЦена животных при продаже:" + ' '.join(map(str, self.sold_animals_price))
        return details
    
class Farm: 
    def __init__(self, contr = Contract(), bank=0, numbers_of_animals=[0,0,0], ava_feed=0):
        self.contract = contr
        self.animals = Animals(numbers_of_animals, ava_feed)
        self.money_capital = bank #денежный капитал фермы
        self.total_capital = bank #общий капитал фермы, включающий животных по цене указанной в контракте
        for i in [animal_const.YOUNG,animal_const.ADULT,animal_const.OLD]:
            self.total_capital += contr.sold_animals_price[i]*numbers_of_animals[i]
    
    def animals_sale(self):
        if len([0 for i,j in zip(self.animals.number, self.contract.sold_animals_number) if i>=j]) == 3:
            self.animals.number[animal_const.YOUNG] -= self.contract.sold_animals_number[animal_const.YOUNG]
            self.animals.number[animal_const.ADULT] -= self.contract.sold_animals_number[animal_const.ADULT]
            self.animals.number[animal_const.OLD] -= self.contract.sold_animals_number[animal_const.OLD]
            for i in [animal_const.YOUNG,animal_const.ADULT,animal_const.OLD]:
                self.money_capital += self.contract.sold_animals_price[i]*self.contract.sold_animals_number[i]
        else:
            for i in [animal_const.YOUNG,animal_const.ADULT,animal_const.OLD]:
                self.animals.number[i] = max(0,self.animals.number[i]-self.contract.sold_animals_number[i])
                self.money_capital += self.contract.sold_animals_price[i]*min(self.animals.number[i],self.contract.sold_animals_number[i])
                self.money_capital -= self.contract.forfeit*(self.contract.sold_animals_number[i]-min(self.animals.number[i],self.contract.sold_animals_number[i]))
            
    def feed_buying(self):
        x = self.contract.feed_price * self.contract.feed_number 
        if self.money_capital>x:
            self.money_capital = self.money_capital - x
            self.animals.ava_feed = self.animals.ava_feed + self.contract.feed_number 
        else:
            n = self.money_capital//self.contract.feed_price
            self.money_capital -= n * self.contract.feed_price
            self.animals.ava_feed += n

    def animals_update(self): #ежегодное изменение числа животных
        self.animals.feeding()
        self.animals.adverse_conditions()
        self.animals.livestock_growth()

    def contract_update(self):
        self.contract.update()

    def capital_update(self):
        self.total_capital = self.money_capital
        for i in [animal_const.YOUNG,animal_const.ADULT,animal_const.OLD]:
            self.total_capital += self.contract.sold_animals_price[i]*self.animals.number[i]

    def bankruptcy(self):
        if (self.total_capital <= 0):
            return True
        return False
    
    def print_details(self):
        details = "\nДенежный капитал:"
        details += str(self.money_capital)
        details += "\nOбщий капитал:"
        details += str(self.total_capital)
        details += self.contract.print_details()
        details += self.animals.print_details()
        return details

class ExternalWorld: # внешний мир
    Farm
    outstring = ""
    begin = True
    
    #считывание данных фермы и контракта
    def reading(self,money,animal_n,feed,remaining_period,feed_number,feed_price,sold_animals_number,sold_animals_price,forfeit):
        bank = int(money)
        number_of_animals = list(map(int,animal_n))
        ava_feed = int(feed)
        self.farm = Farm(self.create_contract(remaining_period,feed_number,feed_price,sold_animals_number,sold_animals_price,forfeit), bank, number_of_animals, ava_feed)
    
    def click_button_step(self,money,animal_n,feed,remaining_period,feed_number,feed_price,sold_animals_number,sold_animals_price,forfeit):
        if self.begin:
            self.reading(money,animal_n,feed,remaining_period,feed_number,feed_price,sold_animals_number,sold_animals_price,forfeit)
            self.begin = False
        if self.farm.contract.remaining_period == 0:
            self.outstring = "\n\nСрок контракта истек, введите новые данные контракта"
            self.begin = True
        else:
            if not (self.farm.bankruptcy()): 
                self.step()
                self.outstring = self.print_details() 
            else:
                self.outstring = "\n\nМы банкроты! Введите новые данные фермы и контракта\n"
                self.begin = True
    
    def click_button_contract(self,money,animal_n,feed,remaining_period,feed_number,feed_price,sold_animals_number,sold_animals_price,forfeit):
        if self.begin:
            self.reading(money,animal_n,feed,remaining_period,feed_number,feed_price,sold_animals_number,sold_animals_price,forfeit)
            self.begin = False
        if self.farm.contract.remaining_period == 0:
            self.outstring = "\n\nСрок контракта истек, введите новые данные контракта"
            self.begin = True
        else:
            if not (self.farm.bankruptcy()): 
                while (self.farm.contract.remaining_period):
                    self.step()
                self.outstring = self.print_details() + "\nСрок контракта истек. Введите данные нового контракта"
                self.begin = True
            else:
                self.outstring = "\n\nМы банкроты! Введите новые данные фермы и контракта\n"
                self.begin = True
        
        
    def step(self): #годовой цикл фермы
        self.farm.feed_buying()
        self.farm.animals_update()
        self.farm.animals_sale()
        self.farm.contract_update()
        self.farm.capital_update()

    def create_contract(self,remaining_period,feed_number,feed_price,sold_animals_number,sold_animals_price,forfeit):
        remaining_period = int(remaining_period)
        feed_number = int(feed_number)
        feed_price = int(feed_price)
        sold_animals_number = list(map(int,sold_animals_number))
        sold_animals_price = list(map(int,sold_animals_price))
        forfeit = int(forfeit)
        return Contract(remaining_period, feed_number, feed_price, sold_animals_number, sold_animals_price, forfeit)

    def print_details(self):
        details = ""
        details += self.farm.print_details() 
        return details