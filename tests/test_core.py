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

    def test_need_beats_greed_regardless_of_value(self):
        rolls = Rolls(2)
        self.assertTrue(rolls.roll("p1", "sword", "greed", 90, 0))
        self.assertTrue(rolls.roll("p2", "sword", "need", 10, 10))
        self.assertEqual(rolls.winner("sword"), "p2")

    def test_need_low_value_still_beats_high_greed_first(self):
        rolls = Rolls(2)
        rolls.roll("p2", "sword", "need", 1, 10)
        rolls.roll("p1", "sword", "greed", 100, 0)
        self.assertEqual(rolls.winner("sword"), "p2")

    def test_higher_value_wins_within_kind(self):
        rolls = Rolls(2)
        rolls.roll("p1", "sword", "greed", 40, 0)
        rolls.roll("p2", "sword", "greed", 70, 10)
        rolls.roll("p3", "sword", "need", 30, 20)
        rolls.roll("p4", "sword", "need", 60, 30)
        self.assertEqual(rolls.winner("sword"), "p4")

    def test_tie_broken_by_player_id_ascending(self):
        rolls = Rolls(2)
        rolls.roll("bob", "sword", "greed", 50, 0)
        rolls.roll("amy", "sword", "greed", 50, 10)
        self.assertEqual(rolls.winner("sword"), "amy")

    def test_one_vote_per_player_per_item(self):
        rolls = Rolls(2)
        self.assertTrue(rolls.roll("p1", "sword", "greed", 50, 0))
        self.assertFalse(rolls.roll("p1", "sword", "greed", 80, 10))
        self.assertFalse(rolls.roll("p1", "sword", "need", 80, 20))
        self.assertEqual(rolls.winner("sword"), "p1")

    def test_same_player_may_vote_on_other_items(self):
        rolls = Rolls(2)
        self.assertTrue(rolls.roll("p1", "sword", "greed", 50, 0))
        self.assertTrue(rolls.roll("p1", "shield", "greed", 50, 10))
        self.assertEqual(rolls.winner("shield"), "p1")

    def test_need_cap_rejects_excess_need(self):
        rolls = Rolls(2)
        self.assertTrue(rolls.roll("p1", "sword", "need", 50, 0))
        self.assertTrue(rolls.roll("p2", "sword", "need", 50, 10))
        self.assertFalse(rolls.roll("p3", "sword", "need", 99, 20))
        self.assertTrue(rolls.roll("p3", "sword", "greed", 99, 30))

    def test_winner_is_isolated_per_item(self):
        rolls = Rolls(2)
        rolls.roll("p1", "sword", "need", 10, 0)
        rolls.roll("p2", "shield", "greed", 90, 10)
        self.assertEqual(rolls.winner("sword"), "p1")
        self.assertEqual(rolls.winner("shield"), "p2")
        self.assertIsNone(rolls.winner("missing"))

    def test_winner_does_not_scan_history(self):
        rolls = Rolls(100000)
        for index in range(1000):
            rolls.roll("p-%d" % index, "item-%d" % index, "greed", 50, index)
        before = rolls.scanned_count()
        for _ in range(1000):
            self.assertEqual(rolls.winner("item-999"), "p-999")
        self.assertEqual(rolls.scanned_count(), before)
        self.assertLessEqual(before, 2000)


if __name__ == "__main__":
    unittest.main()
