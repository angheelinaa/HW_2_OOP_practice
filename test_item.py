import unittest
from item import Item


class TestItem(unittest.TestCase):
    def test_item_id(self):
        'Проверка того что у разных Items разные id'
        item_1 = Item()
        item_2 = Item()
        self.assertNotEqual(item_1.get_id(), item_2.get_id())

    def test_len(self):
        'Проверка того что при добавлении тэгов меняется значение len(item)'
        item = Item()
        item.add_tag("one tag")
        item.add_tag("second tag")
        item.add_tag("third tag")
        self.assertEqual(len(item), 3)

    def test_equal_tags(self):
        'Проверка того что если к предмету добавить два идентичных тега - их колчество будет один'
        item = Item()
        item.add_tag("some tag")
        item.add_tag("some tag")
        self.assertEqual(len(item), 1)

    def test_get_cost(self):
        'Проверка того, что при добавлении предмета с ценой получим значение cost'
        item = Item(cost=72)
        self.assertEqual(item.cost, 72)

    def test_set_cost(self):
        'Проверка того, что при изменении цены у предмета значение cost меняется'
        item = Item(cost=27)
        item.cost = 72
        self.assertEqual(item.cost, 72)

    def test_lt(self):
        'Проверка того, что предмет с большей ценой будет больше, чем предмет с меньшей ценой'
        item_1 = Item(cost=27)
        item_2 = Item(cost=72)
        self.assertTrue(item_1 < item_2)
        self.assertFalse(item_1 > item_2)

    def test_add_tags(self):
        'Проверка того, что в предмет добавляется контейнер из тегов'
        item = Item()
        item.add_tags(['one', 'two', 'three'])
        self.assertEqual(item._tags, {'one', 'two', 'three'})

    def test_rm_tags(self):
        'Провека того, что из предмета удаляется контейнер из тегов'
        item = Item()
        item.add_tags(['one', 'two', 'three'])
        item.rm_tags(['one', 'three'])
        self.assertEqual(item._tags, {'two'})

    def test_is_tagged(self):
        '''Проверка того, что при добавлении одного тега как строка проверится его наличие
        в предмете, а при контейнере из тегов - проверится наличие всех тегов'''
        item = Item()
        item.add_tags(['store', 'of', 'strings'])

        self.assertTrue(item.is_tagged('strings'))
        self.assertFalse(item.is_tagged('string'))

        self.assertTrue(item.is_tagged(['store', 'of', 'strings']))
        self.assertFalse(item.is_tagged(['store', 'of', 'string']))

    def test_copy(self):
        'Проверка того, что возвращается новый item с таким же описанием, ценой и именем, но с другим id'
        item_1 = Item(name='one_item', description='original_item', cost=100)
        item_2 = item_1.copy()
        self.assertNotEqual(item_2.get_id(), item_1.get_id())
        self.assertEqual(item_2.cost, item_1.cost)
        self.assertEqual(item_2.get_name(), item_1.get_name())
        self.assertEqual(item_2._description, item_1._description)
