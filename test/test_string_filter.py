import pathmagic

from string_filter import StringFilter as Filt

import unittest

class StringFilterTestCase(unittest.TestCase):
    """
    Simple tests to verify string filtering functionality
    """
    def setUp(self):
        pass

    def test_contains_raises_TypeError_for_invalid_input(self):
        s = Filt('SomeString')
        self.assertRaises(TypeError, s.contains, 1234)

    def test_contains_returns_false_with_match_case(self):
        s = Filt('SomeString')
        self.assertFalse(s.contains('mest'))

    def test_contains_returns_false_with_match_case(self):
        s = Filt('SomeString')
        self.assertFalse(s.contains(('mest', 'adgf')))

    def test_contains_returns_true_with_match_case(self):
        s = Filt('SomeString')
        self.assertTrue(s.contains('meSt'))

    def test_contains_returns_true_with_no_match_case(self):
        s = Filt('SomeString', False)
        self.assertTrue(s.contains('mest'))

    def test_contains_returns_true_with_tuple(self):
        s = Filt('SomeString')
        self.assertTrue(s.contains(('mest', 'meSt')))

    def test_endswith_raises_TypeError_for_invalid_input(self):
        s = Filt('SomeString')
        self.assertRaises(TypeError, s.endswith, 1234)

    def test_endswith_returns_false_with_str_match_case(self):
        s = Filt('SomeString')
        self.assertFalse(s.endswith('string'))

    def test_endswith_returns_false_with_tuple_match_case(self):
        s = Filt('SomeString')
        self.assertFalse(s.endswith(('string', 'erye')))

    def test_endswith_returns_true_with_str_match_case(self):
        s = Filt('SomeString')
        self.assertTrue(s.endswith('String'))

    def test_endswith_returns_true_with_str_no_match_case(self):
        s = Filt('SomeString', False)
        self.assertTrue(s.endswith('string'))

    def test_endswith_returns_true_with_tuple_match_case(self):
        s = Filt('SomeString')
        self.assertTrue(s.endswith(('String', 'asfasf')))

    def test_endswith_returns_true_with_tuple_no_match_case(self):
        s = Filt('SomeString', False)
        self.assertTrue(s.endswith(('string', 'asdad')))

    def test_equals_raises_TypeError_for_invalid_input(self):
        s = Filt('SomeString')
        self.assertRaises(TypeError, s.equals, 1234)

    def test_equals_returns_false_with_str_match_case(self):
        s = Filt('SomeString')
        self.assertFalse(s.equals('somestring'))

    def test_equals_returns_false_with_tuple_match_case(self):
        s = Filt('SomeString')
        self.assertFalse(s.equals(('somestring', 'asda')))

    def test_equals_returns_true_with_str_match_case(self):
        s = Filt('SomeString')
        self.assertTrue(s.equals('SomeString'))

    def test_equals_returns_true_with_str_no_match_case(self):
        s = Filt('SomeString', False)
        self.assertTrue(s.equals('somestring'))

    def test_equals_returns_true_with_tuple_match_case(self):
        s = Filt('SomeString')
        self.assertTrue(s.equals(('SomeString', 'asda')))

    def test_equals_returns_true_with_tuple_no_match_case(self):
        s = Filt('SomeString', False)
        self.assertTrue(s.equals(('somestring', 'asfd')))

    def test_startswith_raises_TypeError_for_invalid_input(self):
        s = Filt('SomeString')
        self.assertRaises(TypeError, s.startswith, 1234)

    def test_startswith_returns_false_with_str_match_case(self):
        s = Filt('SomeString')
        self.assertFalse(s.startswith('some'))

    def test_startswith_returns_false_with_tuple_match_case(self):
        s = Filt('SomeString')
        self.assertFalse(s.startswith(('some', 'ads')))

    def test_startswith_returns_true_with_str_match_case(self):
        s = Filt('SomeString')
        self.assertTrue(s.startswith('Some'))

    def test_startswith_returns_true_with_str_no_match_case(self):
        s = Filt('SomeString', False)
        self.assertTrue(s.startswith('some'))

    def test_startswith_returns_true_with_tuple_match_case(self):
        s = Filt('SomeString')
        self.assertTrue(s.startswith(('Some', 'asd')))

    def test_startswith_returns_true_with_tuple_no_match_case(self):
        s = Filt('SomeString', False)
        self.assertTrue(s.startswith(('some', 'adf')))

    def test_initialize_with_non_string_input_raises_type_error(self):
        self.assertRaises(TypeError, Filt, 1234)

    def test_initialize_with_non_bool_match_case_raises_type_error(self):
        self.assertRaises(TypeError, Filt, 'asdf', 1234)

    def tearDown(self):
        pass