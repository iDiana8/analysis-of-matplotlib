from itertools import groupby        # импорт функции groupby из itertools (в коде не используется — лишний импорт)
import pandas as pd                  # pandas для работы с таблицами, псевдоним pd
import numpy as np                   # numpy для математики и массивов, псевдоним np
import matplotlib.pyplot as plt      # модуль pyplot из matplotlib, псевдоним plt — для рисования графиков
import seaborn as sns                # seaborn — надстройка над matplotlib для красивых статистических графиков


# 2.1. Столбчатая диаграмма по типам пожаров
df = pd.read_csv('data/FiresRu.csv')                    # читаем CSV-файл в таблицу df
plt.figure()                                        # создаём новую фигуру (новый холст)
df['type_name'].value_counts().plot(kind='bar')     # берём столбец type_name, считаем сколько раз встречается каждое значение, рисуем столбцы
plt.grid()                                          # включаем сетку на графике
plt.savefig('output/1.png')                                # сохраняем фигуру в файл 1.png


# 2.2. Ящик с усами (boxplot) по температуре
plt.figure()                                        # новая фигура
sns.boxplot(x=df['temperature_c'], y=df['type_name'], data=df)  # ящик с усами: по X — температура, по Y — тип пожара
plt.tight_layout()                                  # автоматически подгоняем отступы, чтобы подписи не наезжали
plt.savefig('output/boxplot_by_temperature.png')                                # сохраняем в файл 2.png


# 2.3. Карта пожаров — подготовка данных
plt.figure()                                        # новая фигура
df['lat_lon'] = (df['lat'].astype(int).astype(str) + "-"  # берём широту, округляем до целого (int), превращаем в строку, прибавляем дефис
                 + df['lon'].astype(int).astype(str))     # то же для долготы — получаем ключ вида "131-48"
# 131.5866, 47.8662 -> 131 48 -> "131-48"          # пример: как из координат получается ключ
# grouped = df.groupby(['type_id', 'lat_lon'])['type_name'].count()  # (закомментировано) альтернативный вариант группировки
pivot = pd.pivot_table(data=df, values='type_name',  # строим сводную таблицу: значения — тип пожара,
                       index='lat_lon',              # по строкам — ключ координат,
                       columns='type_id',            # по столбцам — id типа пожара,
                       aggfunc='count')              # в ячейках — количество
grouped = df.groupby('lat_lon').agg({                # группируем по lat_lon и агрегируем:
    'lat': np.mean,                                  # средняя широта для каждой группы,
    'lon': np.mean,                                  # средняя долгота для каждой группы,
})
df = grouped.merge(pivot, how="left", on='lat_lon')  # присоединяем сводную таблицу pivot к grouped по ключу lat_lon
df.to_csv('output/fires.csv')                               # сохраняем результат в новый CSV
type_id = 1                                          # задаём переменную type_id = 1 (будем строить график для этого типа)
plt.scatter(x=df['lon'],                             # точечный график: по X — долгота,
            y=df['lat'],                             # по Y — широта,
            s=df[type_id]*6,                         # размер точки = количество пожаров данного типа * 6 (чтобы было заметно)
            c=df[type_id],                           # цвет точки = количество пожаров (числовая градация)
            cmap='plasma',                           # цветовая карта 'plasma' (от тёмно-синего к жёлтому)
            alpha=0.5)                               # прозрачность 50%
plt.colorbar()                                       # добавляем шкалу цветов справа
plt.show()                                           # показываем график


# 2.4. Тепловая карта корреляций
plt.figure()                                         # новая фигура
df = pd.read_csv('data/FiresRu.csv')                      # снова читаем исходный файл (перезаписываем df)
features = df[[                                       # берём подтаблицу только из нужных столбцов:
    'type_id', 'temperature_c', 'precipitation_mm',
    'relative_humidity', 'wind_speed_ms', 'solar_radiation'
]]
sns.heatmap(features.corr(), annot=True, cmap='coolwarm', fmt='.2f')  # тепловая карта корреляций; annot=True — писать числа в ячейках; coolwarm — цветовая карта сине-красная; fmt='.2f' — 2 знака после запятой
plt.title('Матрица корреляции')                      # заголовок
plt.show()                                           # показываем