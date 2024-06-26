# Система - РСЗВ

[<- main file](../labs/)

За основу взято систему українського походження - БМ21У “Верба” 

![](assets/Pasted%20image%2020240624163247.png)

## Підсистеми

Розбиття системи на функціональні підсистеми

- Система керування вогнем
	- Дозволяє операторам визначати визначення куту запуску ракет, запускати ракети, зупиняти пуск, коригувати, за потреби. 
	- Інтеграція з системами навігації та координації вогню
	- Забезпечення активного коригування вогнем використовуючи дані зовнішніх джерел

- Система балістичних розрахунків
	- Розрахунок параметрів наведення (кут, швидкість ракет, корекція з огляду на погодні умови, рельєф та висоту над рівнем моря)
	- Інтегрування геопросторової системи для симуляції траєкторії політу ракет 

- Система безпеки
	- Забезпечення захисту екіпажу від біологічних, хімічних та радіаційних загроз
	- Інтеграція систем активного та пасивного захисту
	- Моніторинг навколишнього середовища на предмет загроз
	- Забезпечення захисту від дронів (реб)

- Гідравлічна система
	- Забезпечення надійного підйому та спуску (з опор) установки. 
	- Амортизація установки.
	- Автоматизація процесу стабілізації та горизонтування установки

- Паливна система
	- Безпечне зберігання палива
	- Забезпечення подачі палива до двигунів системи
	- Контроль витрат палива, моніторинг рівня палива

- Система транспортування
	- Забезпечення мобільності системи по різних типах місцевості
	- Підтримка стабільного положення системи
	- Захист від перенавантажень під час руху та пуску ракет

- Система звʼязку та навігації
	- Забезпечення звʼязку між операторами установки з командним пунктом (командиром батареї)
	- Інтеграція з суміжними пусковими
	- Забезпечення захисту комунікацій
	- Визначення географічного положення установки
	- Інтеграція з системами GPS та координування

- Система електроживлення
	- Забезпечення незалежного живлення усіх систем установки
	- Керування розподілом енергії між підсистемами
	- Аварійне відключення живлення при детектуванні збоїв

- Контрольно-діагностична система
	- Моніторинг стану всіх підсистем РСЗВ
	- Діагностика збоїв та виявлення несправностей
	- Монітринг стану ракет та пускової установки 
	- Ведення журналу подій системи (аля логування подій системи) 


##  Structure Diagram

![](assets/sysml.png)


## Requirements Diagram

![](assets/reqd.png)

## Use Case

![](assets/uml.png)


## State Diagram

Main diagram

![](assets/State.png)

Power diagram

![](assets/state_power.png)

FireControl System

![](assets/state_firecontrol.png)


Defence

![](assets/state_def.png)

Fuel system

![](assets/state_fuel.png)


## Sequences diagram

![](assets/seq_main.png)

![](assets/seq_start.png)

![](assets/seq_hydravlics.png)

![](assets/seq_diagnostic.png)

![](assets/seq_panorama.png)

![](assets/seq_kyt.png)

![](assets/seq_firetype.png)

![](assets/seq_rockets.png)


![](assets/seq_firemode.png)

![](assets/seq_fiire.png)

![](assets/seq_fiirestop.png)

![](assets/seq_firemodeoff.png)

![](assets/seq_stop.png)

## Activity diagram

![](assets/activity.png)

## Python Implementation

Швидкій перехід
- [Стартовий файл](src/main.py)
- [Клас шасі та повʼязаного](src/Vehicle.py)
- [Клас контролю вогню](src/FireControl.py)
- [Клас оператора](src/Operator.py)
- [Клас ракет](src/Missile.py)
- [Клас журналу подій](src/EventLog.py)

Приклад запуску

![](assets/Pasted%20image%2020240629140005.png)

Логування цих самих дій

![](assets/Pasted%20image%2020240629135952.png)


