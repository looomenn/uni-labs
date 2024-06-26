---
Course: ADS4
Points: 1 / 8
Variant: 1
Dedline: 2024-04-06
Done?: true
---
---

[<- Home](../)

### Objectives

Слова тексту із малих латинських літер записані не менше, ніж через
один пробіл; текст закінчується крапкою. Написати програму введення
такого тексту з клавіатури та його обробки, використовуючи: 
- [x] масив
- [x] список

Загальний алгоритм розв’язання поставленої задачі, як правило, не
залежить від конкретної реалізації структури даних. Але **всі** дії над текстом
(пошук слів, виділення будь-якого із слів, перестановка літер в слові тощо)
повинні бути описані функціями,  «налаштованими» на конкретну реалізацію
з допомогою формальних параметрів.

- [x] Надрукувати всі слова, у яких непарна кількість літер. Перед друком
видалити першу та останню літеру кожного слова. До кожного слова
дописати кому.


### Technical requirements

```zsh
conda create --name ads python=3.11
```

```zsh
conda install pyinputplus numpy
```


### Appendix

**Файли**
- [ASD_Lab3.doc](doc/ASD_Lab3.doc)
- [main.py](src/main.py)
