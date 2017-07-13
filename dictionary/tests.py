import unittest

from . import match, navigate, reshape, serialize, transform, types

nested = {
    'name': 'Joe',
    'age': 55,
    'hobbies': [{'name': 'boxing'}, {'name': 'tennis'}],
    'scores': {
        'tetris': 9000,
        'bubbles': 2705,
    },
}

flat = {
    'name': 'Joe',
    'age': 55,
    'hobbies': [{'name': 'boxing'}, {'name': 'tennis'}],
    'scores_tetris': 9000,
    'scores_bubbles': 2705,
}

records = [
    {
        'name': 'Joe',
        'gender': 'male',
        'industry': 'military',
        'age': 55,
    }, {
        'name': 'Tom',
        'gender': 'male',
        'industry': 'services',
        'age': 23,
    }, {
        'name': 'Fran',
        'gender': 'female',
        'industry': 'services',
        'age': 78,
    }
]

indexed_records = dict(zip(
    ('joe', 'tom', 'fran'),
    records,
))


class TestHumanize(unittest.TestCase):
    def test_slugify(self):
        pass

    def test_humanize(self):
        pass

class TestMatch(unittest.TestCase):
    def test_matches(self):
        pass

    def test_equals(self):
        pass

class TestNavigate(unittest.TestCase):
    def test_pluck(self):
        pass

    def test_find(self):
        pass

    def test_traverse(self):
        pass

class TestReshape(unittest.TestCase):
    def test_deflate(self):
        dictionary.deflate(nested)

    def test_inflate(self):
        dictionary.inflate(flat)

    def test_columns(self):
        pass

    def test_records(self):
        pass

class TestSerialize(unittest.TestCase):
    def test_simplify(self):
        pass

class TestTransform(unittest.TestCase):
    def test_whitelist(self):
        pass

    def test_blacklist(self):
        pass

    def test_pick(self):
        pass

    def test_omit(self):
        pass

    def test_intersection(self):
        pass

    def test_union(self):
        pass

    def test_transform_keys_by_predicate(self):
        pass

    def test_transform_keys_by_mapping(self):
        pass

    def test_transform_keys_by_function(self):
        transformed = transform.transform(
            records[0],
            keys=lambda key: key.upper(),
            )
        self.assertEqual(set(transformed.keys()), {'NAME', 'AGE'})

    def test_transform_values_by_predicate(self):
        pass

    def test_transform_values_by_mapping(self):
        pass

    def test_transform_values_by_function(self):
        pass

    def test_transform_keys_by_function_deeply(self):
        transformed = transform.transform(
            nested,
            keys=lambda key: key.upper(),
            deep=True,
        )
        self.assertIn('SCORES', transformed)
        self.assertEqual(set(transformed['SCORES'].keys()), {'TETRIS', 'BUBBLES'})

    def test_clone_deeply(self):
        pass

    def test_groupby(self):
        pass

    def test_indexby(self):
        pass

    def test_indexby_strict(self):
        pass

    def test_indexby_last(self):
        pass


class TestTypes(unittest.TestCase):
    def test_sort(self):
        pass

    def test_options(self):
        pass


if __name__ == '__main__':
    unittest.main()
