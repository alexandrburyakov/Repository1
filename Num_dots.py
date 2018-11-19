"""
Программа оценивает количество точек на изображении.
На начальном этапе изображение переводится в формат оттенков серого(grayscale) и представляется в виде массива(np.array), который
переводится в двоичный (binary) формат с использованием порогового значения (threshold), полученного путем нахождения
среднего значения от максиамального и минимального значений элементов массива.(В общем случае величина порога может быть вычеслена
более универсальным методом, например нахождением минимального значения на гистограмме,построенной на наборе значений 
массива 'grayscale'-изображения.)
Далее к данному массиву применяется функция (measurements.label()), которая подсчитывает количество объектов на изображении и выдает
лэйбл-массив, присваивая каждому элементу массива каждого объекта определенное значение - лэйбл объекта. Переменной num_dots 
присваивается значение количества объектов.
Далее, с помощью лэйбл-массива рассчитывается количество элементов массива в каждом объекте изображения (Counter(labels)), и 
определяется количество элементов как в наименьшем, так и в наибольшем объекте. При этом количество нулей (количество элементов фона)
в объекте Counter занижается до нуля, чтобы не влиять на дальнейшие расчеты.
После этого устанавливаются 3 лимита для количества элементов массива в каждом объекте изображения, позволяющие разделить объекты на 
4 группы, как состоящие из 1-й, 2-х, 3-х или 4-х точек. При этом лимиты устанавливаются следующим образом: limit1 - количество 
элементов в наименьшем объекте плюс 10%, limit2 = limit1 + int((maxlabels_counter - limit1)*0.33), 
limit3 = limit1 + int((maxlabels_counter - limit1)*0.66), где maxlabels_counter - количество элементов массива изображения в 
наибольшем объекте.
В заключении запускается цикл, сортирующий объекты изображения по 3-м группам (наименьшие объекты из первой группы не учитываются), 
при этом, при попаданиии объекта в группу между limit1 и limit2 значение num_dots увеличивается на 1, при попаданиии объекта в 
группу между limit2 и limit3 значение num_dots увеличивается на 2, а при попадании объекта в группу выше значение num_dots 
значение num_dots увеличивается на 3.
Окончательное значение переменной num_dot - искомая оценка количества точек на изображении.
"""
from urllib import request
from collections import Counter
from PIL import Image
from numpy import *
from scipy.ndimage import measurements

#Загрузка изображения 
url = "https://lh5.googleusercontent.com/yO12GARP3fqmNOZ00zM9Q_nyBVWWfR_xVu8skrvAmhB1hzSJyq_F593jhQqS48aWJyCZ5jzDAQ=w513"
img = request.urlopen(url)

#Конвертирование в формат оттенков серого и преобразование в массив
im = array(Image.open(img).convert('L'))

#Расчет порога и преобразование в черно-белый binary формат
im_1d = im.flatten()
minim_1d = min(im_1d)
maxim_1d = max(im_1d)
threshold = minim_1d +(maxim_1d - minim_1d)/2
im = 1*(im < threshold)

#расчет количества объектов и лэйбл-массива
labels, nbr_objects = measurements.label(im)
num_dots = nbr_objects
     
#определение количества элементов массива у наименьшего и наибольшего объектов
labels = labels.flatten()
labels_counter = Counter(labels)
minlabels_counter = min(labels_counter.values())
labels_counter[0] = 0
maxlabels_counter = max(labels_counter.values())

#расчет лимитов
limit1 = int(minlabels_counter*1.1)
limit2 = limit1 + int((maxlabels_counter - limit1)*0.33)
limit3 = limit1 + int((maxlabels_counter - limit1)*0.66)


#распределение объектов по группам
for k in range(1,max(labels)+1):
    if labels_counter[k] > limit1 and labels_counter[k] <= limit2:
        num_dots += 1
    if labels_counter[k] > limit2 and labels_counter[k] <= limit3:
        num_dots += 2
    if labels_counter[k] > limit3:
        num_dots += 3

print ('Num Dots =',num_dots)

