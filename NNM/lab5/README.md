# Классификация изображений. Сверточные сети. Полносвязные сети с предобучением.
## Задание
Дан набор данных изображений цветов, состоящий из 5 классов.
1. Построить сверточную нейронную сеть из нескольких пар слоев: Conv2D и MaxPooling, максимальной длинны, допустимой приведенной размерностью входных изображений. В качестве выходных слоев применить двухслойную послносвязную сеть, позволяющую классифицировать на 5 классов.
2. Построить полносвязную нейронную сеть, позволяющую классифицировать на 5 классов исходный набор данных изображений цветов. Для улучшения точности обучения и валидации использовать метод преобучения без учителя с применением автокодировщика.
3. Сравнить полученные точности и потери для построенных сверточной и полносвязной сетей на этапах обучения и валидации.