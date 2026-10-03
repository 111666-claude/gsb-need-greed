"""需求分配：需求优先、掷点比较、平局按玩家 id、每人一票与需求票上限。

每件物品单独维护投票索引与当前赢家：投票是 O(1) 增量更新，
winner 直接返回缓存赢家，不扫描历史投票。
"""


_KIND_RANK = {"greed": 0, "need": 1}


class Rolls:
    def __init__(self, max_need):
        self.max_need = max_need
        self._items = {}
        self.scanned = 0

    def roll(self, player, item, kind, value, at_ms):
        state = self._items.get(item)
        if state is None:
            state = {"votes": {}, "need": 0, "best": None}
            self._items[item] = state
        if player in state["votes"]:
            return False
        if kind == "need" and state["need"] >= self.max_need:
            return False
        state["votes"][player] = (kind, value)
        if kind == "need":
            state["need"] += 1
        self.scanned += 1
        best = state["best"]
        if best is None or self._beats(player, kind, value, best, *state["votes"][best]):
            state["best"] = player
        return True

    @staticmethod
    def _beats(player, kind, value, other_player, other_kind, other_value):
        rank = _KIND_RANK[kind]
        other_rank = _KIND_RANK[other_kind]
        if rank != other_rank:
            return rank > other_rank
        if value != other_value:
            return value > other_value
        return player < other_player

    def winner(self, item):
        state = self._items.get(item)
        return None if state is None else state["best"]

    def scanned_count(self):
        return self.scanned
