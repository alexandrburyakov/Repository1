"""
Восcтанови длину карусели. (Задание с одного из соревнований по программированию).

Рекомендательная система должна эффективно определять интересы людей. И помимо методов машинного обучения, 
для выполнения этой задачи используются специальные интерфейсные решения, которые явным образом спрашивают пользователя, что ему интересно.
Одним из таких решений является карусель.

Карусель — это горизонтальная лента из карточек, каждая из которых предлагает подписаться на конкретный источник или тему. 
Одна и та же карточка может встречаться в карусели несколько раз. Карусель можно прокручивать слева направо, 
при этом после последней карточки пользователь снова видит первую. 
Для пользователя переход от последней карточки к первой незаметен, с его точки зрения лента бесконечна.

В какой-то момент любопытный пользователь Василий заметил, что лента на самом деле зациклена, и решил выяснить истинную длину карусели. 
Для этого он стал прокручивать ленту и последовательно выписывать встречающиеся карточки, для простоты обозначая каждую карточку 
строчной латинской буквой. Так Василий выписал первые n карточек на листок бумаги. 
Гарантируется, что он просмотрел все карточки карусели хотя бы один раз. Потом Василий лёг спать, а утром обнаружил, 
что кто-то пролил стакан с водой на его записи и некоторые буквы теперь невозможно распознать.

По оставшейся информации помогите Василию определить наименьшее возможное количество карточек в карусели.

Формат ввода
В первой строке задано одно целое число n — количество символов, выписанных Василием.
Вторая строка содержит выписанную Василием последовательность. Она состоит из n
символов — строчных букв латинского алфавита и знака #, который обозначает, что букву на этой позиции невозможно распознать.

Формат вывода
Выведите одно целое положительное число — наименьшее возможное количество карточек в карусели.
"""
length = input() #Ввод количества символов
string = input() #Ввод последовательности
length = int(length)

def first_char(length, string):
"""
Функция, определяющая положение первого буквы в последовательности (на случай если в начале стоят символы '#')
"""
    k = 0
    sign = 0
    while k < length and sign == 0:
        if string[k] == '#':
            k += 1
        else: 
            sign = 1
    if k == length:
        return 'n'
    else:
        return k

def char_comp(j, cnt_i, string, length):
"""
Функция сравнивает две последовательности длиной cnt_i, причем первая начинается с индекса 'j', а вторая с ледует за ней.
"""
    i_last = j + cnt_i
    for i in range(j, i_last):
        if i+cnt_i < length:
            if string[i] != string[i+cnt_i] and string[i] != '#' and string[i+cnt_i] != '#':
                return False
        if i+cnt_i == length:
            return True
        return True

k = first_char(length, string)

#Сравнение всех возможных последовательностей длиной от 1 до length - k.
if k != 'n':
    for cnt_i in range(1, length - k):
        for j in range(k, length, cnt_i):
            rez = char_comp(j, cnt_i, string, length)
            if not rez:
                break
        if rez:
            break
else:
    cnt_i = 1

print(cnt_i)