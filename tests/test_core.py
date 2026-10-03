import unittest

from loot.core import Rolls


class BasicTest(unittest.TestCase):
    def test_empty_winner(self):
        self.assertIsNone(Rolls(2).winner("sword"))

    def test_single_roll_wins(self):
        rolls = Rolls(2)
        rolls.roll("p1", "sword", "greed", 50, 0)
        self.assertEqual(rolls.winner("sword"), "p1")

    def test_max_need_is_stored(self):
        self.assertEqual(Rolls(3).max_need, 3)

    def test_scanned_starts_at_zero(self):
        self.assertEqual(Rolls(2).scanned_count(), 0)


if __name__ == "__main__":
    unittest.main()
