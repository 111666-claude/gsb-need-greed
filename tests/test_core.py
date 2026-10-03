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


class NeedGreedTest(unittest.TestCase):
    def test_need_beats_higher_greed(self):
        rolls = Rolls(2)
        rolls.roll("p1", "sword", "greed", 90, 0)
        rolls.roll("p2", "sword", "need", 10, 10)
        self.assertEqual(rolls.winner("sword"), "p2")

    def test_higher_value_wins_within_same_kind(self):
        rolls = Rolls(2)
        rolls.roll("p1", "sword", "need", 30, 0)
        rolls.roll("p2", "sword", "need", 70, 10)
        self.assertEqual(rolls.winner("sword"), "p2")
        rolls = Rolls(2)
        rolls.roll("p1", "sword", "greed", 70, 0)
        rolls.roll("p2", "sword", "greed", 30, 10)
        self.assertEqual(rolls.winner("sword"), "p1")

    def test_tie_breaks_by_player_id_ascending(self):
        rolls = Rolls(2)
        rolls.roll("bob", "sword", "greed", 50, 0)
        rolls.roll("amy", "sword", "greed", 50, 10)
        self.assertEqual(rolls.winner("sword"), "amy")

    def test_duplicate_roll_rejected(self):
        rolls = Rolls(2)
        self.assertTrue(rolls.roll("p1", "sword", "greed", 50, 0))
        self.assertFalse(rolls.roll("p1", "sword", "greed", 80, 10))
        self.assertEqual(rolls.winner("sword"), "p1")

    def test_same_player_can_roll_on_other_items(self):
        rolls = Rolls(2)
        self.assertTrue(rolls.roll("p1", "sword", "greed", 50, 0))
        self.assertTrue(rolls.roll("p1", "shield", "greed", 50, 10))

    def test_max_need_caps_need_rolls(self):
        rolls = Rolls(2)
        self.assertTrue(rolls.roll("p1", "sword", "need", 10, 0))
        self.assertTrue(rolls.roll("p2", "sword", "need", 20, 10))
        self.assertFalse(rolls.roll("p3", "sword", "need", 30, 20))
        self.assertTrue(rolls.roll("p3", "sword", "greed", 30, 30))
        self.assertEqual(rolls.winner("sword"), "p2")

    def test_scanned_does_not_grow_linearly(self):
        rolls = Rolls(100000)
        for index in range(3000):
            rolls.roll("p-%d" % index, "item-%d" % index, "greed", 50, index)
        for _ in range(3000):
            rolls.winner("item-2999")
        self.assertLessEqual(rolls.scanned_count(), 6000)


if __name__ == "__main__":
    unittest.main()
