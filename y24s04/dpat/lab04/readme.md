---
Course: DPAT4
Points: "? / 10"
Variant: 1
Dedline: 2024-04-13
Done?: true
---
---

[<- Home](../)

### Objectives

Перший рівень
- [x] Виконати всі завдання, використовуючи як numpy array, так і dataframe
- [x] Проаналізувати часові витрати на виконання процедур (профілювання часу виконання)
- [x] Зробити висновки щодо ситуацій, в яких має сенс віддати перевагу тій чи іншій структурі даних. Висновки оформити звітом із зазначеним часом виконання та оцінкою по 5-бальній шкалі зручності виконання операцій відбору).
- [x] Звернути увагу на те, що дані, як і практично все в реальному житті, можуть потребувати Вашої уваги - потрібно залишити лише ті спостереження, в яких немає порожніх спостережень (порожні значення – пусті поля між роздільником – ? – 28.04.2007, як приклад).
- [x] Реалізувати наступне:
	- [x] 1. Обрати всі домогосподарства, у яких загальна активна споживана потужність перевищує 5 кВт.
	- [x] 2. Обрати всі домогосподарства, у яких вольтаж перевищує 235 В.
	- [x] 3. Обрати всі домогосподарства, у яких сила струму лежить в межах 19-20 А, для них виявити ті, у яких пральна машина та холодильних споживають більше, ніж бойлер та кондиціонер.
	- [x] 4. Обрати випадковим чином 500000 домогосподарств (без повторів елементів вибірки), для них обчислити середні величини усіх 3-х груп споживання електричної енергії.
	- [x] 4.1. Обрати ті домогосподарства, які після 18-00 споживають понад 6 кВт за хвилину в середньому, серед відібраних визначити ті, у яких основне споживання електроенергії у вказаний проміжок часу припадає на пральну машину, сушарку, холодильник та освітлення (група 2 є найбільшою), а потім обрати кожен третій результат із першої половини та кожен четвертий результат із другої половин.


Другий рівень
- [x] Обрати [датасет](https://archive.ics.uci.edu/ml/index.php/) згідно наступних умов:
	- Data Set Characteristics: Multivariate
	- Attribute Characteristics: Categorical, Integer, Real
	- Number of Attributes: at least 2 integers/real
	- Missing Values? YES!!!!!
- [x] Виконати всі завдання, використовуючи як numpy array, так і dataframe
- [x] Поборотися із зниклими даними.
- [x] Пронормувати вибраний датасет або стандартизувати його
	- нормалізація і стандартизація мають бути реалізовані як окремі функції без застосування додаткових бібліотек, як наприклад sklearn.preprocessing)
- [x] Збудувати гістограму по одному із атрибутів, що буде показувати на кількість елементів, що знаходяться у 10 діапазонах, які ви задасте.
- [x] Збудувати графік залежності одного integer/real атрибута від іншого.
- [x] Підрахувати коефіцієнт Пірсона та Спірмена для двох integer/real атрибутів.
- [x] Провести One Hot Encoding категоріального string атрибуту.
- [x] Провести візуалізацію багатовимірних даних, використовуючи приклади, наведені у [медіумі](https://towardsdatascience.com/the-art-of-effective-visualization-of-multi-dimensional-data-6c7202990c57)


### Technical requirements


```
conda create --name da python=3.11
```

```
conda activate da
```

```
pip install jupyterlab notebook pandas matplotlib numpy seaborn scipy
```


### Appendix

- [level1](src/level1.ipynb)
- [level2](src/level2.ipynb)

#### Перший рівень

Для запису часу виконання кожного завдання будемо використовувати контектменеджер

```python
@contextmanager
def timer(lib: str, task: str):
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        time_used = round(end - start, 6)
        record(lib, task, time_used)
        
        print(f'task: {task:}\nlib: {lib}\ntime used: {time_used}')
```

Наприклад, перший таск

```python
# task: 0
# lib: pandas

with timer('pandas', 'task0'):
    pd_data = pd.read_csv(URL, sep=';', na_values='?')
    pd_data.dropna(inplace=True)

pd_data.head()
```

Це все записується в словник `TIMER: dict = {'lib': {'task1': 3.5, ...}, ...`

Результати операцій

![](assets/Pasted%20image%2020240604135230.png)

![](assets/Pasted%20image%2020240604135242.png)

Можна побачити, що pandas набагато ефективніше імпортує дані з файлу, навідміну від numpy (різниця в 10 разів). Решта операцій +- однаково.

Загальна таблиця:

![](assets/Pasted%20image%2020240604135630.png)

Щодо зручності:
- pandas - 5 / 5 
- numpy - 3 / 5
	- багато пейн з масками бо якось по іншому не працює...

#### Другий рівень
Обраний датасет

https://archive.ics.uci.edu/dataset/45/heart+disease

![](assets/Pasted%20image%2020240602203638.png)

![](assets/Pasted%20image%2020240602203820.png)

Результат парного графіку

![](assets/Pasted%20image%2020240604165859.png)

