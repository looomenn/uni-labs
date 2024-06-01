---
Course: DPAT4
Points: "? / 10"
Variant: 1
Dedline: 2024-04-13
Done?:
---
---

[<- Home](../)

### Objectives

- [ ] Обрати [датасет](https://archive.ics.uci.edu/ml/index.php/) згідно наступних умов:
	- Data Set Characteristics: Multivariate
	- Attribute Characteristics: Categorical, Integer, Real
	- Number of Attributes: at least 2 integers/real
	- Missing Values? YES!!!!!
- [ ] Виконати всі завдання, використовуючи як numpy array, так і dataframe
- [ ] Поборотися із зниклими даними.
- [ ] Пронормувати вибраний датасет або стандартизувати його
	- нормалізація і стандартизація мають бути реалізовані як окремі функції без застосування додаткових бібліотек, як наприклад sklearn.preprocessing)
- [ ] Збудувати гістограму по одному із атрибутів, що буде показувати на кількість елементів, що знаходяться у 10 діапазонах, які ви задасте.
- [ ] Збудувати графік залежності одного integer/real атрибута від іншого.
- [ ] Підрахувати коефіцієнт Пірсона та Спірмена для двох integer/real атрибутів.
- [ ] Провести One Hot Encoding категоріального string атрибуту.
- [ ] Провести візуалізацію багатовимірних даних, використовуючи приклади, наведені у [медіумі](https://towardsdatascience.com/the-art-of-effective-visualization-of-multi-dimensional-data-6c7202990c57)


### Technical requirements


```
conda create --name da python=3.11
```

```
conda activate da
```

```
pip install pandas matplotlib numpy seaborn scipy scikit-learn
```


### Appendix