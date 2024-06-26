---
Course: ADS4
Points: "? / 10"
Variant: 1
Dedline: 2024-04-27
Done?:
---
---

[<- Home](../)

### Objectives

**1 частина**
- [x] Розробити програму роботи з чергою, яка реалізує операції додавання, видалення елементів з черги і відображення поточного стану черги. 
	- [x] Реалізувати чергу двома способами: 
		- [x] за допомогою масиву (кільцеву чергу) 
		- [x] списку 

**2 частина**
- [x] Перетворіть наведені нижче вирази у постфіксну форму і реалізуйте за допомогою стеку: 

1. $$\frac{(A-B-C)}{D} - E*F$$
2. $$(A+B)*C - \frac{(D+E)}{F}$$
3. $$\frac{A}{(B-C)}+D*(E-F)$$
4. $$\frac{(A*B+C)}{D}-\frac{F}{E}$$

### Technical requirements

```zsh
conda create --name ads python=3.11
```

```zsh
conda install pyinputplus python-dotenv
```

### Appendix

- [Файл умови](doc/ads_lab04.pdf)
- [Виконання](src/main.py)


### Приклад виконання

Початкове меню вибору мови. З'являється щоразу при запуску. Значення мови зберігається в `.env` файлі (Якщо `getenv('LANG')` не спрацює, то дефолтно буде встановлена Українська мова)

![](assets/Pasted%20image%2020240521172523.png)

Наприклад, вибираємо Українську. Самі переклади знаходяться в окремому JSON файлі.

![](assets/Pasted%20image%2020240521172706.png)

Далі нас вітає головне меню, де ми можемо вибрати, яке завдання переглянути. **Почнемо з черг.**

Оскільки умовою було реалізація черги двома методами, наступне меню дає нам можливість вибрати, який метод використовувати. 

![](assets/Pasted%20image%2020240521172945.png)


Наприклад, кільцева (там трошки більше функціоналу). Як тільки ми вибрали її, нам падає інпут на визначення розміру черги.

![](assets/Pasted%20image%2020240521173233.png)


Далі нас зустрічає меню (аля пульт-кервання) чергою, де можна зробити відповідні дії з ініціалізованою чергою. 

![](assets/Pasted%20image%2020240521173314.png)

Найкраща можливість, звісно, додати декілька елементів одразу

![](assets/Pasted%20image%2020240521173817.png)

Через особливість кільцевої черги (оскільки ми задавали розмір), елементи, які додаються після заповнення черги будуть ігноровані. 

Видалення елементу з черги

![](assets/Pasted%20image%2020240521203331.png)

Та стан черги

![](assets/Pasted%20image%2020240521203351.png)

Для "списочної" черги (черга, яка використовує список) аналогічний пункт буде виводити лише вміст. 


Тепер рівняння

![](assets/Pasted%20image%2020240521203524.png)

Приклади рівнянь (де-факто, це рівняння з умови [Objectives](Objectives (частина 2)))

![](assets/Pasted%20image%2020240521203807.png)

Рівняння задаються в словнику, інфіксним методом.

```python
equations: dict = {
	'example': {
		'infix': '(((A - B) * C) + (D / (E + F)))',
		'supports_evaluation': False
	}
}
```

Було зроблено також обмеження - `supports_evaluation is True` тільки для рівнянь, які складаються лише з цифр. 

Тепер саме цікаво, можливість введення свого рівняння

![](assets/Pasted%20image%2020240521204317.png)

![](assets/Pasted%20image%2020240521204338.png)

Аналогічне обмеження - обчислення результату працює тільки для рівнянь, що складаються лише з цифр. Тут також приклад перевірки, щоб не було поєднання змінних та цифр в одному рівнянні.

![](assets/Pasted%20image%2020240521204437.png)

Заради тестування, також був доданий regex проти усіх непотрібних символів.. 

![](assets/Pasted%20image%2020240521204541.png)

```python
[^0-9A-Za-z\s()+\-*/]
```

Тобто, дозволено: цифри, літери, пробіл, дужки та символи арифметичних дій

Єдине, що не вдалося перекласти, так це відповіді від бібліотеки `pyinputplus`

![](assets/Pasted%20image%2020240521204745.png)

Бо тоді це треба писати кастомну функцію на валідацію під кожен інпут... 

