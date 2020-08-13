#!/usr/bin/python3
""" """
import unittest
import pep8
from models.user import User

class Test_user(unittest.TestCase):
    """ """

    def test_pep8_User(self):
        """Tests pep8 style"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/user.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_checking_for_docstring_User(self):
        """test docstrings"""
        self.assertIsNotNone(User.__doc__)

if __name__ == "__main__":
    unittest.main()
