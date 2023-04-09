import unittest
import datetime
from hub import Hub
from item import Item


class TestHub(unittest.TestCase):
    def setUp(self):
        'Создаем экземпляр класса Hub для каждого теста'
        self.h = Hub()

    def test_hub_singleton(self):
        'Проверка того что hub - синглтон'  # небольшая документация к тесту
        self.assertTrue(Hub() is Hub())

    def test_len(self):
        'Проверка того что при добавлении предметов меняется значение len(item)'
        for i in range(5):
            self.h.add_item(Item())
        self.assertEqual(len(self.h), 5)

    def tearDown(self):
        'Обнуляем экземпляр класса Hub после каждого теста'
        self.h.reset()

    def test_getitem(self):
        'Проверка того, что по hub можно итерироваться и получать правильные item по индексу'
        item = Item()
        self.h.add_item(item)
        self.assertEqual(self.h[0], self.h._items[0])

    def test_find_by_id(self):
        'Проверка того, что по id возвращаются правильные item и индекс, если нет такого id - (-1, None)'
        item = Item()
        item_1 = Item()
        self.h.add_item(item)
        self.assertEqual(self.h.find_by_id(item.get_id()), (0, item))
        self.assertEqual(self.h.find_by_id(item_1.get_id()), (-1, None))

    def test_find_by_tags(self):
        'Проверка того, что возвращаются все item с данными тегами'
        item_1 = Item()
        item_2 = Item()
        item_1.add_tag('one')
        item_2.add_tag('one')
        item_2.add_tag('two')
        self.h.add_item(item_1)
        self.h.add_item(item_2)
        self.assertEqual(self.h.find_by_tags(['one', 'two']), [item_2])

    def test_rm_item(self):
        '''Проверка того, что если вводим id - удаляется предмет с таким id,
        если вводим предмет - удаляется этот предмет'''
        item_1 = Item()
        item_2 = Item()
        self.h.add_item(item_1)
        self.h.rm_item(item_1.get_id())
        self.assertEqual(len(self.h), 0)
        self.h.add_item(item_2)
        self.h.rm_item(item_2)
        self.assertEqual(len(self.h), 0)

    def test_drop_items(self):
        'Проверка того, что предметы из контейнера items удалятся в _items Hub'
        item_1 = Item()
        item_2 = Item()
        item_3 = Item()
        items_1 = [item_2, item_3]
        items_2 = [item_1, Item()]
        self.h.add_item(item_1)
        self.h.add_item(item_2)
        self.h.add_item(item_3)

        self.h.drop_items(items_1)
        self.assertEqual(len(self.h), 1)

        self.h.drop_items(items_2)
        self.assertEqual(len(self.h), 0)

    def test_clear(self):
        'Проверка того, что при удалении всех предметов в items len(hub) будет = 0'
        for i in range(5):
            self.h.add_item(Item())
        self.h.clear()
        self.assertEqual(len(self.h), 0)

    def test_add_item(self):
        'Проверка того, что в hub не добавится предмет не типа Item'
        self.h.add_item('item')
        self.assertEqual(len(self.h), 0)

    def test_find_most_valuable(self):
        '''Проверка того, что при amount < количества предметов возвращается список
        дорогих item, а при amount > количества предметов - целиком items'''
        item_1 = Item(cost=100)
        item_2 = Item(cost=10)
        item_3 = Item(cost=200)
        self.h.add_item(item_1)
        self.h.add_item(item_2)
        self.h.add_item(item_3)
        self.assertEqual(self.h.find_most_valuable(2), [item_3, item_1])
        self.h.rm_item(item_3)
        self.h.rm_item(item_1)
        self.assertEqual(self.h.find_most_valuable(), [item_2])

    def test_find_by_date(self):
        '''Проверка того, что при одном аргументе возвращается список item с датой раньше,
        при двух аргументах - список item с датами между аргументами, при большем количестве
        аргументов - ошибка'''
        item_1 = Item()
        item_2 = Item()
        item_3 = Item()
        self.h.add_item(item_1)
        self.h.add_item(item_2)
        self.h.add_item(item_3)
        self.assertEqual(self.h.find_by_date(datetime.datetime.now()), [item_1, item_2, item_3])
        self.assertEqual(self.h.find_by_date(datetime.datetime.now(), datetime.datetime.now()), [])
        with self.assertRaises(Exception):
            self.h.find_by_date(datetime.datetime.now(), datetime.datetime.now(), datetime.datetime.now())
