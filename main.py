import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('sales.csv')

#СОЗДАНИЕ ХОЛСТА
fig, ax = plt.subplots(1, 2, figsize=(14, 5), layou='constrained')

#РИСОВАНИЕ
#ЛИНЕЙНЫЙ ГРАФИК
ax[0].plot(
    df['month'],
    df['sales'],
    marker='o',
    linestyle='-',
    color='steelblue',
    linewidth=2,
    label='Продажи'
)
#ОФОРМЛЕНИЕ
ax[0].set_title('Продажи по месяцам')
ax[0].set_xlabel('Месяц')
ax[0].set_ylabel('Сумма, руб.')
ax[0].grid(True, alpha=0.3, linestyle='--')
ax[0].legend()

#СТОЛБЧАТАЯ ДИАГРАММА
ax[1].bar(
    df['month'],
    df['sales'],
    color='coral',
    label='Продажи'
)
ax[1].set_title('Продажи по месяцам (столбчатая)')
ax[1].set_xlabel('Месяц')
ax[1].set_ylabel('Сумма, руб.')
ax[1].grid(True, axis='y', alpha=0.3)
ax[1].legend()

#ОТОБРАЖЕНИЕ
fig.savefig('out.png')
plt.show()
