from hub import Hub
import re
from item import Item


h = Hub()
h.clear()
h.add_item(Item(name='Часы', cost=10_000))
h.add_item(Item(name='Антифриз', cost=2000))
h.add_item(Item(name='Свеча', cost=1000))
h.add_item(Item(name='Лампа', cost=1500))
h.add_item(Item(name='Игрушка для кота', cost=300))
h.add_item(Item(name='Скетчбук', cost=2500))
h.add_item(Item(name='Коврик для йоги', cost=3000))
h.add_item(Item(name='Проектор', cost=15_000))
h.add_item(Item(name='Микрофон', cost=6000))
h.add_item(Item(name='Книга', cost=500))
h.add_item(Item(name='Картина', cost=800))
h.add_item(Item(name='антиквар', cost=20_000))
h.add_item(Item(name='Крем', cost=5000))
h.add_item(Item(name='Планшет', cost=7000))
h.add_item(Item(name='Коврик для мыши', cost=1000))

A = [i for i in h if re.match('[аА]', i.get_name())]
h.drop_items(A)

Outdated = h.find_by_date(h.date)
h.drop_items(Outdated)

MostValuable = h.find_most_valuable(10)
h.drop_items(MostValuable)

Others = [i for i in h]


