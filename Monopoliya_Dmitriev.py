from colorama import Fore, Back, Style, init
from random import randint, shuffle
from time import sleep
from os import system
from playsound import playsound

init()


def print_cash(cash: int):
    cash = str(cash)
    s = []
    if len(cash)%3:
        s.append(cash[: len(cash)%3])
        cash = cash[len(cash)%3 :]
    while cash:
        s.append(cash[: 3])
        cash = cash[3 :]
    return ",".join(s)


def print_color(text, color):
    if color == "RED":
        return Fore.RED+text+Fore.WHITE
    if color == "BLUE":
        return Fore.BLUE+text+Fore.WHITE
    if color == "GREEN":
        return Fore.GREEN+text+Fore.WHITE
    if color == "MAGENTA":
        return Fore.MAGENTA+text+Fore.WHITE
    if color == "YELLOW":
        return Fore.YELLOW+text+Fore.WHITE
    if color == "CYAN":
        return Fore.CYAN+text+Fore.WHITE
    if color == "WHITE":
        return Fore.WHITE+text+Fore.WHITE


def standart_print(board, players):
    def print_board(board, players):
        def print_one(board, players, indx):
            fishki_in_place = "" # фишки игроков в place, нужно для сохранения пробелов
            for player in players:
                if player[5] == indx:
                    fishki_in_place += print_color(player[1], player[2])

            if len(fishki_in_place) > 0:
                fishki_in_place = " " * (5 - int(len(fishki_in_place)//11)) + fishki_in_place
            else:
                fishki_in_place = " "*5

            houses = "" # обозначаем дома
            tablichka = "[" # и таблички
            colors = ("RED", "BLUE", "GREEN", "YELLOW", "MAGENTA", "CYAN")
            color = "WHITE"
            place = board[indx][0]
            if len(board[indx]) == 9: # собственность, но не магнит и пятёрочка
                for player in players:
                    if player[0] == board[indx][1]:
                        color = player[2]
                        break
                houses = board[indx][4]*"•"
                tablichka = Style.BRIGHT + print_color("|", colors[(board[indx][6] - 1)%6]) + Style.RESET_ALL
                place = print_color(place, color)
                if board[indx][8]:
                    place = Back.WHITE + place + Back.BLACK
            elif len(board[indx]) == 7: # магнит или пятёрочка
                for player in players:
                    if player[0] == board[indx][1]:
                        color = player[2]
                        break
                tablichka =  Style.BRIGHT + "|" + Style.RESET_ALL
                place = print_color(place, color)
                if board[indx][6]:
                    place = Back.WHITE + place + Back.BLACK                     # реальная длина place
            print(fishki_in_place + tablichka + place + houses, end = " "*(33 - len(board[indx][0]) - len(houses)))

        for start in range(9):
            for indx in range(start, (len(board)//4*3)+1+start, 9):
                print_one(board, players, indx)
            print()


    print()
    print_board(board, players)
    print("------------------------")
    max_len_name = max(len(player[0]) for player in players) # длина самого большого имени
    max_len_cash = max(len(print_cash(player[3])) for player in players) # длина самого большого бюждета
    for i in players: # вывод бюджетов
        print(" "*(max_len_name - len(i[0])), end = "")
        print(print_color(i[0], i[2]), end = ": ") # вывод имени
        print(" "*(max_len_cash - len(print_cash(i[3]))), end = "")
        print(print_cash(i[3]) + "₽; " + "₽" + print_cash(all_money(i, board)))
    print("------------------------") # выводит доску и бюджеты


def name_verbs(verb):
    if verb == go: return "Бросить кости"
    elif verb == sell_houses: return "Продать дома"
    elif verb == buy_place: return "Купить недвижимость"
    elif verb == zalog: return "Заложить недвижимость"
    elif verb == buy_houses: return "Купить дом"
    elif verb == anti_zalog: return "Вернуть заложенную недвижемость"
    elif verb == aukcion: return "Начать аукцион"


def all_money(player, board): # возвращает бюджет с игрока после продажи домов и заложения недвижимости, player - players[n]
    nedviz = 0
    for i in board:
        if len(i) == 9 and (i[1] == player[0]) and not(i[8]):
            nedviz += sum(i[5][:i[4]]) + i[7]
        if len(i) == 7 and (i[1] == player[0]) and not(i[6]):
            nedviz += i[5]
    return nedviz + player[3]


def go(indx): # бросить кости
    playsound('sound/kubi.mp3', False)
    sleep(1)
    kub1 = randint(1, 6)
    print(kub1)
    sleep(0.6)
    kub2 = randint(1, 6)
    print(kub2)
    sleep(0.5)
    condition = False # пройден круг или нет для получения денег за прохождения круга
    for step in range(kub1 + kub2):
        sleep(0.1)
        players[indx][5] += 1
        if players[indx][5] >= len(board): # если пройден кург
            players[indx][5] %= len(board)
            condition = True
        system("cls")
        standart_print(board, players)
        print("Выпало: ")
        print(kub1)
        print(kub2)
    if condition:
        print(print_color(players[indx][0], players[indx][2]) + ", вы прошли круг и получаете 2000 ₽")
        input("Нажмите ENTER, чтоб получить деньги")
        players[indx][3] += 2000
        system("cls")
        standart_print(board, players)


def sell_houses(indx): # запускать только если есть дома для продажи
    houses = [ [i[0], i[4]] for i in board if (len(i) == 9 and i[1] == players[indx][0] and i[4] != 0)]
    while True:
        print("У тебя есть дома в:")
        n = 0
        for i in houses:
            n += 1
            print(str(n) + ".", i[0] + ":", i[1], "штук")
        where = 0
        while where not in [str(i+1) for i in range(len(houses))]:
            print("Напиши номер недвижимости, где хочешь продать дом: ", end = "")
            where = input()

        count = 0
        if houses[int(where)-1][1] == 1:
            count = 1
        else:
            while count not in [str(i+1) for i in range(houses[int(where)-1][1])]:
                print("Сколько шочешь продать домов?")
                count = input()
        text = ""
        for i in range(len(board)):
            if board[i][0] == houses[int(where)-1][0]:
                players[indx][3] += sum(board[i][5][ board[i][4] - int(count) : board[i][4]])
                text += "Ты продал " +  str(count) + "домов в " + str(board[i][0]) + "и получил: ₽" + print_cash(sum(board[i][5][ board[i][4] - int(count) : board[i][4]]))+"\n"
                board[i][4] -= int(count)
        system("cls")
        standart_print(board, players)
        print(text)
        houses = [ [i[0], i[4]] for i in board if (len(i) == 9 and i[1] == players[indx][0] and i[4] != 0)]
        if len(houses):
            vibor = ""
            while vibor not in ("1", "2"):
                vibor = input("Хочешь ещё продать дома?\n1. Да\n2. Нет\n")
            if vibor == "2":
                break
        else:
            break


def buy_place(indx): # запускать если есть деньги на недвижимость и она свободна
    playsound('sound/buy.mp3', False)
    board[players[indx][5]][1] = players[indx][0]
    players[indx][3] -= board[players[indx][5]][2]
    system("cls")
    standart_print(board, players)
    print(print_color(players[indx][0], players[indx][2]), "купил", '"' + board[players[indx][5]][0] + '"', "за ₽" + print_cash(board[players[indx][5]][2]))
    print("Нажмите ENTER для продолжения")
    input()


def zalog(indx): # запускать если есть что закладыать
    nedviz = []
    for place in board:
         if len(place) == 9 and place[1] == players[indx][0] and place[4] == 0 and not(place[8]):
             nedviz.append(place)
         elif len(place) == 7 and place[1] == players[indx][0] and not(place[6]):
              nedviz.append(place)
    while len(nedviz):
        print("Ты можешь заложить:")
        for i in range(len(nedviz)):
            if len(nedviz[i]) == 9:
                print(str(i+1)+".", '"' + nedviz[i][0] + '"', "за ₽" + print_cash(nedviz[i][7]))
            else:
                print(str(i+1)+".", '"' + nedviz[i][0] + '"', "за ₽" + print_cash(nedviz[i][5]))
        vibor = []
        while len(set(vibor)) != len(vibor) or vibor == [] or not(all([i in [str(j+1) for j in range(len(nedviz))] for i in vibor])):
            vibor = input("Введи через пробел номера недвижимости, которую хотел бы заложить\n").split()
        for i in vibor:
            for j in range(len(board)):
                if board[j][0] == nedviz[int(i)-1][0]:
                    if len(board[j]) == 9:
                        board[j][8] = True
                        players[indx][3] += board[j][7]
                        print("Ты заложил", '"'+board[j][0]+'"', "за ₽" + print_cash(board[j][7]))
                        break
                    elif len(board[j]) == 7 and not(board[j][6]):
                        board[j][6] = True
                        players[indx][3] += board[j][5]
                        print("Ты заложил", '"'+board[j][0]+'"', "за ₽" + print_cash(board[j][5]))
                        break
        system("cls")
        standart_print(board, players)
        nedviz = []
        for place in board:
             if len(place) == 9 and place[1] == players[indx][0] and place[4] == 0 and not(place[8]):
                 nedviz.append(place)
             elif len(place) == 7 and place[1] == players[indx][0] and not(place[6]):
                  nedviz.append(place)
        if len(nedviz):
            vibor = ""
            while vibor not in ("1", "2"):
                vibor = input("Желаешь ещё что-то заложить?\n1. Да\n2.Нет\n")
            if vibor == "2":
                break
        else:
            break


def anti_zalog(indx): # запускать если есть что раззалаживать и есть деньги на это
    where = [] # номера мест которые можно раззаложить и на это хватает денег
    for i in range(len(board)):
        if len(board[i]) not in (7, 9): continue # если это не собственность
        if len(board[i]) == 9 and board[i][8] and board[i][1] == players[indx][0] and board[i][7] <= players[indx][3]:
            where.append(i)
        elif len(board[i]) == 7 and board[i][6] and board[i][1] == players[indx][0] and board[i][5] <= players[indx][3]:
            where.append(i)
    while True:
        print("Ты можешь вернуть:")
        for i in range(len(where)):
            if len(board[where[i]]) == 9:
                print(str(i+1) + ".", board[where[i]][0], "за ₽" + print_cash(board[where[i]][7]))
            else:
                print(str(i+1) + ".", board[where[i]][0], "за ₽" + print_cash(board[where[i]][5]))
        vibor = ""
        while vibor not in [str(i+1) for i in range(len(where))]:
            vibor = input("Введите номер недвижимости: ")
        if len(board[where[int(vibor)-1]]) == 9:
            board[where[int(vibor)-1]][8] = False
            players[indx][3] -= board[where[i]][7]
        else:
            board[where[int(vibor)-1]][6] = False
            players[indx][3] -= board[where[i]][5]
        system("cls")
        standart_print(board, players)
        where.remove(where[int(vibor) - 1]) # убираем из списка индекс того места, которое только что вернули из залога
        if len(where):
            vibor = ""
            print("Хочешь ещё что-то вернуть из залога?\n1. Да\n2. Нет\n")
            while vibor not in ("1", "2"):
                vibor = input()
            if vibor == "2": break
        else:
            break


def buy_houses(indx): # запускать если есть где строить дома и есть деньги на них
    type = 1
    where_all = [] # индексы мест где можно построить дом
    where = []
    for n in range(len(board)):
        if len(board[n]) != 9: continue
        if board[n][6] == type:
            if board[n][1] == players[indx][0] and not(board[n][8]):
                where.append(n)
                if len(where) == 3:
                    for i in where:
                        if board[i][4] < 4 and board[i][5][board[i][4]] <= players[indx][3]:
                            where_all.append(i)
                    type += 1
                    where = []
            else:
                type += 1
                where = []
    print("Ты можешь построить дом в:")
    n = 0
    for i in where_all:
        n += 1
        print(str(n) + ".", board[i][0])
    vibor = ""
    while vibor not in [str(i+1) for i in range(len(where_all))]:
        vibor = input("Введите номер:")
    playsound('sound/built.mp3', False)
    players[indx][3] -= board[where_all[int(vibor)-1]][5][board[where_all[int(vibor)-1]][4]]
    board[where_all[int(vibor)-1]][4] += 1
    system("cls")
    standart_print(board, players)


def aukcion(indx):
    print("Аукцион начался, начальная цена — ₽10")
    who_want = [[player, True] for player in players if (player[6] == "в игре" and all_money(player, board) > 10)]
    price = 10
    n = -1
    condition = False # условие что все участники аукциона были спрошены хотя бы 1 раз
    while (len([i for i in who_want if i[1]]) > 1) or not(condition):
        n += 1
        if n == len(who_want):
            n = 0
        if not who_want[n][1]: continue
        player = who_want[n][0]
        if all_money(player, board) > price:
            vibor = ""
            print(print_color(player[0], player[2]) + ", ты можешь:")
            while vibor not in ("1", "2"):
                vibor = input("1. Преложить цену выше\n2. Закончить участие в аукционе\n")
            if vibor == "1":
                new_price = ""
                while not(new_price.isdigit() and int(new_price) > price and int(new_price) <= all_money(player, board)):
                    new_price = input(print_color(player[0], player[2]) + ", предложи цену выше ₽" + print_cash(price) + ": ")
                price = int(new_price)
            else:
                who_want[n][1] = False
        else:
            who_want[n][1] = False
        if n == len(who_want) - 1: condition = True
    if price > 10:
        system("cls")
        standart_print(board, players)
        for A in who_want:
            if (not A[1]): continue
            for j in range(len(players)):
                if not (players[j][0] == A[0][0]): continue
                if players[j][3] < price: # если надо что-то проадть для получения суммы которую указал в аукционе
                    print(print_color(players[j][0], players[j][2]), "ты победитель аукциона, но тебе надо что-то продать чтоб купить недвижимость")
                    verbs = make_verbs_list(3, j)
                    while True: # пока нет денег на покупку
                        print(print_color(players[j][0], players[j][2]), "тебе доступны действия:")
                        for i in range(len(verbs)):
                            print(str(i+1) + ".", name_verbs(verbs[i]))
                        vibor = ""
                        while vibor not in [str(i+1) for i in range(len(verbs))]:
                            vibor = input("Введи номер действия: ")
                        verbs[int(vibor)-1](j)
                        if players[j][3] >= price:
                            break
                        verbs = make_verbs_list(3, j)
                playsound('sound/buy.mp3', False)
                board[players[indx][5]][1] = players[j][0]
                players[j][3] -= price
                system("cls")
                standart_print(board, players)
                print(print_color(players[j][0], players[j][2]), "купил", '"' + board[players[indx][5]][0] + '"', "за ₽" + print_cash(price))
                input("Нажмите ENTER для продолжения")


def make_verbs_list(situaciya, indx): # situaciya: 1 - старт, ход ещё не сделан; 2 - ход сделан, попали на что-то но денег хватает,
    nedviz = []                                  # 3 - денег не хватает, нельзя устроить аукцион нужно продавать, закладывать... 4 - на надвижимости, денег не хватает
    for place in board: # недвижимость которую можно заложить
         if len(place) == 9 and place[1] == players[indx][0] and place[4] == 0 and not(place[8]):
             nedviz.append(place)
         elif len(place) == 7 and place[1] == players[indx][0] and not(place[6]):
              nedviz.append(place)

    houses = [ [i[0], i[4]] for i in board if (len(i) == 9 and i[1] == players[indx][0] and i[4] != 0)] # есть дома

    type = 1
    where_all = [] # где можно построить дом
    where = []
    for n in range(len(board)):
        if len(board[n]) != 9: continue
        if board[n][6] == type:
            if board[n][1] == players[indx][0] and not(board[n][8]):
                where.append(n)
                if len(where) == 3:
                    for i in where:
                        if board[i][4] < 4 and board[i][5][board[i][4]] <= players[indx][3]:
                            where_all.append(i)
                    type += 1
                    where = []
            else:
                type += 1
                where = []

    where_was_zalog = [] # номера мест которые можно раззаложить и на это хватает денег
    for i in range(len(board)):
        if len(board[i]) not in (7, 9): continue
        if len(board[i]) == 9 and board[i][8] and board[i][1] == players[indx][0] and board[i][7] <= players[indx][3]:
            where_was_zalog.append(i)
        elif len(board[i]) == 7 and board[i][6] and board[i][1] == players[indx][0] and board[i][5] <= players[indx][3]:
            where_was_zalog.append(i)

    if situaciya == 1:
        verbs = [go] # доступные действия
        if len(nedviz):
            verbs.append(zalog)
        if len(houses):
            verbs.append(sell_houses)
        if len(where_all):
            verbs.append(buy_houses)
        if len(where_was_zalog):
            verbs.append(anti_zalog)
    elif situaciya == 2:
        verbs = [buy_place, aukcion]
    elif situaciya == 3:
        verbs = []
        if len(nedviz):
            verbs.append(zalog)
        if len(houses):
            verbs.append(sell_houses)
    elif situaciya == 4:
        verbs = []
        if all_money(players[indx], board):
            if len(nedviz):
                verbs.append(zalog)
            if len(houses):
                verbs.append(sell_houses)
            if len([[player, True] for player in players if (player[6] == "в игре" and all_money(player, board) > 10)]):
                verbs.append(aukcion)
    return verbs


print("\tЭто монополия Дмитриева! В правилах разберёшься сам, в этом городе важен фарт и умение пользоваться деньгами!!!\n")
start_cash = 10_000 # стартовая сумма у игроков
count_bots = ""
while (count_bots not in ("0", "1", "2", "3")):
    count_bots = input("Введите кол-во ботов (от 0 до 3): ")
count_players = ""
while (count_players not in [str(i) for i in range(1, 5+1 - int(count_bots))]):
    count_players = input("Введите кол-во игрунов (от 1 до " + str(5 - int(count_bots)) + "): ")
flag = True
players = []
bots_name = ["Бот-словоглот", "Ботус", "the La Бот"] # имена которые могут получить боты
while flag: # пока не введены корректные имена
    players = []
    fishki = ["☻", "♥", "♦", "♣", "♫"]
    colors = ["RED", "BLUE", "GREEN", "YELLOW", "MAGENTA"]
    shuffle(fishki)
    shuffle(colors)
    for i in range(int(count_players)):
        # print("Введите имя", str(i+1) + "-го игрока: ", end = "")
        # player = [input(), fishki.pop(0), colors.pop(0), start_cash, 0, 0, "в игре"]
        player = [input(f"Введите имя {str(i+1)}-го игрока: "), fishki.pop(0), colors.pop(0), start_cash, 0, 0, "в игре"]
         #          имя       фишка          цвет         бюджет    ходов    координата   состояние(в игре, в тюрьме, банкрот)
         #           0          1              2             3        4           5            6
        players.append(player)                                 #в тюрьме осталось
    if len([i[0] for i in players]) == len(set([i[0] for i in players])) and ("" not in [i[0] for i in players]) and (not(any([i[0] in bots_name for i in players]))):
        flag = False
    else:
        print("Ваши имена совпадают, придумайте другие!")
for i in range(int(count_bots)): # добавляем ботов
    bot = [bots_name[i], fishki.pop(0), colors.pop(0), start_cash, 0, 0, "в игре"]
    players.append(bot)
shuffle(players) # делаем случайным порядок ходов

for player in players:
    print(player[0]+",", "твоя фишка и цвет:", print_color(player[1], player[2]))
    sleep(1)
sleep(2)
    #     0          1         2          3           4               5            6                   7                          8
    # название   владелец    цена       рента     кол-во домов    цены домов    категория    денег получишь за залог            в залоге True
board = [["Cтарт"], # +2000                                                               # (та жа сумма для выкупа из залога)  не в залогге False
         ["Миллиметрово", "", 500, (50, 180, 390, 700, 1500), 0, (200, 400, 800, 1200), 1, 400, False],
         ["Дом на дереве", "", 600, (50, 200, 450, 900, 1600), 0, (200, 400, 800, 1200), 1, 400, False],
         ["Погребок", "", 600, (60, 200, 450, 900, 1600), 0, (200, 400, 800, 1200), 1, 400, False],
         ["Прогрессивный налог"], # -25%
#                 0           1      2               3                     4         5       6
# как аэропорт [название, владелец, цена, (рента с 1..4 "аэропортами"), категория, залог, состояние]
         ["Пятёрочка", "", 2000, (500, 1000, 2000, 3000), 9, 1000, False],
         ["Кинотеатр", "", 800, (90, 220, 500, 1000, 1800), 0, (250, 500, 1000, 1450), 2, 500, False],
         ["ЦДТ", "", 800, (90, 220, 500, 1000, 1800), 0, (250, 500, 1000, 1450), 2, 500, False],
         ["ДК", "", 1000, (100, 250, 550, 1100, 2000), 0, (300, 600, 1100, 1600), 2, 500, False],

         ["Cтоянка"],
         ["Центральный парк", "", 1200, (120, 280, 600, 1350, 2250), 0, (350, 700, 1300, 1900), 3, 800, False],
         ["Аллея", "", 1200, (120, 280, 600, 1350, 2250), 0, (350, 700, 1300, 1900), 3, 800, False],
         ["Магнит", "", 2000, (500, 1000, 2000, 3000), 9, 1000, False], # как аэропорт [название, владелец, цена, (рента с 1..4 "аэропортами"), категория, залог, состояние]
         ["Большой парк", "", 1200, (120, 280, 600, 1350, 2250), 0, (350, 700, 1300, 1900), 3, 800, False],
         ["Жизнь миллионера"], # +200
         ["Шаурмишная", "", 1500, (150, 400, 900, 1500, 2500), 0, (400, 800, 1400, 2200), 4, 1200, False],
         ["Ларёк привокзальный", "", 1500, (150, 400, 900, 1500, 2500), 0, (400, 800, 1400, 2200), 4, 1200, False],
         ["Пиццерия", "", 1500, (150, 400, 900, 1500, 2500), 0, (400, 800, 1400, 2200), 4, 1200, False],

         ["Тюрьма"], # пропуск 7 ходов или штраф 500
         ["Мираж", "", 2000, (200, 500, 1000, 1800, 3000), 0, (500, 900, 1600, 2500), 5, 1500, False],
         ["Марго", "", 2000, (200, 500, 1000, 1800, 3000), 0, (500, 900, 1600, 2500), 5, 1500, False],
         ["Пятёрочка", "", 2000, (500, 1000, 2000, 3000), 9, 1000, False], # как аэропорт [название, владелец, цена, (рента с 1..4 "аэропортами"), категория, залог, состояние]
         ["Канцлер", "", 2000, (200, 500, 1000, 1800, 3000), 0, (500, 900, 1600, 2500), 5, 1500, False],
         ["Жизнь миллионера"], # +200
         ["Школа", "", 2500, (350, 900, 1500, 2400, 3500), 0, (700, 1000, 1800, 2800), 6, 2000, False],
         ["Шарага", "", 2500, (350, 900, 1500, 2400, 3500), 0, (700, 1000, 1800, 2800), 6, 2000, False],
         ["Речевуха", "", 2500, (350, 900, 1500, 2400, 3500), 0, (700, 1000, 1800, 2800), 6, 2000, False],

         ["Cтоянка"],
         ["Автовокзал", "", 2800, (400, 1000, 1700, 2800, 4000), 0, (800, 1200, 2200, 3100), 7, 2400, False],
         ["ЖД вокзал", "", 2800, (400, 1000, 1700, 2800, 4000), 0, (800, 1200, 2200, 3100), 7, 2400, False],
         ["Такси", "", 2800, (400, 1000, 1700, 2800, 4000), 0, (800, 1200, 2200, 3100), 7, 2400, False],
         ["Налог"], # -1000
         ["Больница", "", 3200, (500, 1200, 2000, 3400, 4500), 0, (1000, 1400, 2500, 3500), 8, 2800, False],
         ["Магнит", "", 2000, (500, 1000, 2000, 3000), 9, 1000, False], # как аэропорт [название, владелец, цена, (рента с 1..4 "аэропортами"), категория, залог, состояние]
         ["Почта", "", 3200, (500, 1200, 2000, 3400, 4500), 0, (1000, 1400, 2500, 3500), 8, 2800, False],
         ["Пункт выдачи", "", 3200, (500, 1200, 2000, 3400, 4500), 0, (1000, 1400, 2500, 3500), 8, 2800, False],
        ]
system("cls")


# начало игры, игра до тех пор, пока не останется один не обанкротившийся игрок
indx = -1 # индекс игрока, делающего ход
while len(players) - len([status_player[6] for status_player in players if status_player[6] == "банкрот"]) > 1:
    standart_print(board, players)
    indx += 1 # игроки ходят по очереди
    if indx >= len(players):
        indx = 0
    if players[indx][6] == "банкрот":
        system("cls")
        continue
    elif players[indx][6] == "в тюрьме":
        players[indx][4] -= 1
        if players[indx][4] == 0:
            print("Вы просидели 7 дней в тюрьме, ваш срок окончен")
            players[indx][6] = "в игре"
        elif players[indx][3] >= 500:
            print(print_color(players[indx][0], players[indx][2]), "вам осталось сидеть в тюрьме", players[indx][4], "дней.\nВаш выбор:")
            cho = ""
            while cho not in ("1", "2"):
                print("1. Сидеть дальше")
                print("2. Заплатить ₽500 и выйти сейчас")
                cho = input()
            if cho == "1":
                system("cls")
                continue
            else:
                players[indx][3] -= 500
                players[indx][4] = 0
                players[indx][6] = "в игре"
        else:
            print(print_color(players[indx][0], players[indx][2]), "вам осталось сидеть в тюрьме", players[indx][4], "дней и у вас нет денег для взятки.\nНажмите ENTER чтоб передать ход")
            input()
            system("cls")
            continue

    verbs = make_verbs_list(1, indx)
    condition = False
    while True: # пока не бросил кости
        if len(verbs) == 1:
            input(print_color(players[indx][0], players[indx][2]) + " нажмите ENTER чтоб бросить кости")
            go(indx)
            break
        print(print_color(players[indx][0], players[indx][2]), "тебе доступны действия:")
        for i in range(len(verbs)):
            print(str(i+1) + ".", name_verbs(verbs[i]))
        vibor = ""
        while vibor not in [str(i+1) for i in range(len(verbs))]:
            vibor = input("Введи номер действия: ")
        verbs[int(vibor)-1](indx)
        if verbs[int(vibor)-1] == go:
            break
        elif verbs[int(vibor)-1] == buy_houses:
            condition = True
        verbs = make_verbs_list(1, indx)
        if condition and buy_houses in verbs:
            verbs.remove(buy_houses)
    # куда-то попал
    if board[players[indx][5]][0] == "Жизнь миллионера":
        print(print_color(players[indx][0], players[indx][2]) + ", вы попали в " + '"Жизнь миллионера", получите ₽200')
        input("Нажмите ENTER чтоб передать ход")
        players[indx][3] += 200
    elif board[players[indx][5]][0] == "Cтоянка":
        print(print_color(players[indx][0], players[indx][2]) + ", вы попали в " + '"Стоянку", ничего не делайте')
        input("Нажмите ENTER чтоб передать ход")
    elif board[players[indx][5]][0] == "Прогрессивный налог":
        print(print_color(players[indx][0], players[indx][2]) + ", вы попали в " + '"Прогрессивный налог", это 25% ваших наличных\nНажмите ENTER чтоб заплатить ₽' + print_cash((players[indx][3]//4//10)*10))
        input()
        players[indx][3] -= (players[indx][3]//4//10)*10
    elif board[players[indx][5]][0] == "Тюрьма":
        players[indx][4] = 7
        players[indx][6] = "в тюрьме"
        print("Вы в тюрьме! 7 дней посидите пока")
        input("Нажмите ENTER")
    elif board[players[indx][5]][0] == "Налог":
        if players[indx][3] >= 2000:
            input("Заплати налог ₽2,000\nНажмите ENTER")
            players[indx][3] -= 2000
        elif all_money(players[indx], board) >= 2000:
            verbs = make_verbs_list(3, indx)
            while True:
                print(print_color(players[indx][0], players[indx][2]), "тебе доступны действия:")
                for i in range(len(verbs)):
                    print(str(i+1) + ".", name_verbs(verbs[i]))
                vibor = ""
                while vibor not in [str(i+1) for i in range(len(verbs))]:
                    vibor = input("Введи номер действия: ")
                verbs[int(vibor)-1](indx)
                if players[indx][3] >= 2000:
                    players[indx][3] -= 2000
                    break
                verbs = make_verbs_list(3, indx)
        else:
            input("Вы банкрот! Прощайте\nНажмите ENTER")
            for i in len(board):
                if len(board[i]) in (7, 9) and board[i][1] == players[indx][0]:
                    board[i][1] = ""
                    if len(board[i]) == 9:
                        board[i][8] = False
                    else:
                        board[i][6] = False
                    players[indx][6] = "банкрот"
    elif len(board[players[indx][5]]) in (7, 9): # недвижимость
        if board[players[indx][5]][1] == "": # ничейная собственность
            print("Вы попали в", '"' + board[players[indx][5]][0] + '"', "стоимость: ₽" + print_cash(board[players[indx][5]][2]))
            if players[indx][3] >= board[players[indx][5]][2]:
                verbs = make_verbs_list(2, indx)
                vibor = ""
                for i in range(len(verbs)):
                    print(str(i+1) + ".", name_verbs(verbs[i]))
                while vibor not in [str(i+1) for i in range(len(verbs))]:
                    vibor = input(print_color(players[indx][0], players[indx][2]) + ", введи номер действия: ")
                verbs[int(vibor)-1](indx)
                if board[players[indx][5]][1] == "": #если выбрали аукцион но никто не купил
                    buy_place(indx)
            elif all_money(players[indx], board) >= board[players[indx][5]][2]:
                print("Сразу купить не выйдет")
                verbs = make_verbs_list(4, indx)
                while board[players[indx][5]][1] == "": # пока кто-то не купил
                    print(print_color(players[indx][0], players[indx][2]), "тебе доступны действия:")
                    for i in range(len(verbs)):
                        print(str(i+1) + ".", name_verbs(verbs[i]))
                    vibor = ""
                    while vibor not in [str(i+1) for i in range(len(verbs))]:
                        vibor = input("Введи номер действия: ")
                    verbs[int(vibor)-1](indx)
                    if players[indx][3] >= board[players[indx][5]][2]:
                        buy_place(indx)
                        break
                    verbs = make_verbs_list(4, indx)
            else:
                if len([[player, True] for player in players if (player[6] == "в игре" and all_money(player, board) > 10)]):
                    print("У тебя нет денег, придёся устроить аукцион")
                    aukcion(indx)
                if board[players[indx][5]][1] == "":
                    input(print_color(players[indx][0], players[indx][2]) + ", вы банкрот! Прощайте\nНажмите ENTER")
                    for i in range(len(board)):
                        if len(board[i]) in (7, 9) and board[i][1] == players[indx][0]:
                            board[i][1] = ""
                            if len(board[i]) == 9:
                                board[i][8] = False
                            else:
                                board[i][6] = False
                            players[indx][6] = "банкрот"
        elif board[players[indx][5]][1] != players[indx][0]: # чья-то собственность, но не ходящего
            for i in range(len(players)):
                if players[i][0] == board[players[indx][5]][1]:
                    vladelec = players[i] # владелец недвижимости
                    break
            if vladelec[6] == "в тюрьме":
                input(print_color(players[indx][0], players[indx][2]) + ", повезло тебе, ведь владелец отбывает срок и не может получать ренту\nНажмите ENTER") # ничего не делаем, если владелец в тюрьме
            elif len(board[players[indx][5]]) == 9 and not(board[players[indx][5]][8]): # не пятёрка и магнит и не в залоге
                renta = board[players[indx][5]][3][board[players[indx][5]][4]]
                       # (нет домов в этом месте)                         невижемость, если len = 9  (игрок indx владеет всеми 3-мя недвижимостью этой категории)
                if board[players[indx][5]][4] == 0 and sum([1 for i in board if (len(i) == 9 and i[6] == board[players[indx][5]][6] and i[1] == vladelec[0])]) == 3 :
                    renta *= 2                            # и не в залоге
                print("Вы попали в", '"' + board[players[indx][5]][0] + '"', "заплатите владельцу", print_color(vladelec[0], vladelec[2]), "₽" + print_cash(renta))
                if players[indx][3] >= renta:
                    players[indx][3] -= renta
                    vladelec[3] += renta
                    input("Нажмите ENTER")
                elif all_money(players[indx], board) > renta:
                    print("Вам придётся что-то продать")
                    verbs = make_verbs_list(3, indx)
                    while True:
                        print(print_color(players[indx][0], players[indx][2]), "тебе доступны действия:")
                        for i in range(len(verbs)):
                            print(str(i+1) + ".", name_verbs(verbs[i]))
                        vibor = ""
                        while vibor not in [str(i+1) for i in range(len(verbs))]:
                            vibor = input("Введи номер действия: ")
                        verbs[int(vibor)-1](indx)
                        if players[indx][3] >= renta:
                            players[indx][3] -= renta
                            vladelec[3] += renta
                            break
                        verbs = make_verbs_list(3, indx)
                else:
                    input("Вы банкрот! Прощайте\nНажмите ENTER")
                    for i in len(board):
                        if len(board[i]) in (7, 9) and board[i][1] == players[indx][0]:
                            board[i][1] = ""
                            if len(board[i]) == 9:
                                board[i][8] = False
                            else:
                                board[i][6] = False
                            players[indx][6] = "банкрот"
            elif len(board[players[indx][5]]) == 7 and not(board[players[indx][5]][6]): # пятёрка и магнит
                renta = (500, 1000, 2000, 3000)[sum([1 for i in board if (len(i) == 7 and i[1] == vladelec[0] )]) - 1]
                print("Вы попали в", '"' + board[players[indx][5]][0] + '"', "заплатите владельцу", print_color(vladelec[0], vladelec[2]), "₽" + print_cash(renta))
                if players[indx][3] >= renta:
                    players[indx][3] -= renta
                    vladelec[3] += renta
                    input("Нажмите ENTER")
                elif all_money(players[indx], board) > renta:
                    print("Вам придётся что-то продать")
                    verbs = make_verbs_list(3, indx)
                    while True:
                        print(print_color(players[indx][0], players[indx][2]), "тебе доступны действия:")
                        for i in range(len(verbs)):
                            print(str(i+1) + ".", name_verbs(verbs[i]))
                        vibor = ""
                        while vibor not in [str(i+1) for i in range(len(verbs))]:
                            vibor = input("Введи номер действия: ")
                        verbs[int(vibor)-1](indx)
                        if players[indx][3] >= renta:
                            players[indx][3] -= renta
                            vladelec[3] += renta
                            break
                        verbs = make_verbs_list(3, indx)
                else:
                    input("Вы банкрот! Прощайте\nНажмите ENTER")
                    for i in len(board):
                        if len(board[i]) in (7, 9) and board[i][1] == players[indx][0]:
                            board[i][1] = ""
                            if len(board[i]) == 9:
                                board[i][8] = False
                            else:
                                board[i][6] = False
                            players[indx][6] = "банкрот"
            else:
                input("Повезло тебе, эта собственность в залоге\nНажми ENTER")
        else:
            playsound("sound/SweetHome.mp3", False)
            input("Ты в своей собственности, чувствуй себя как дома!\nНажми ENTER")
    system("cls")

# вывод победителя
for i in players:
    if i[6] == "в игре":
        print("Победитель: " + i[0])
        input()
        break
