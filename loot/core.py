"""需求分配：需求优先、掷点、平局按玩家 id、每人一票与需求票上限。"""


_KIND_RANK = {"greed": 0, "need": 1}


class Rolls:
    def __init__(self, max_need):
        self.max_need = max_need
        self._items = {}
        self.scanned = 0

    def roll(self, player, item, kind, value, at_ms):
        if kind not in _KIND_RANK:
            raise ValueError("unknown kind: %r" % (kind,))
        state = self._items.get(item)
        if state is None:
            state = {"players": set(), "need": 0, "best": None}
            self._items[item] = state
        if player in state["players"]:
            return False
        if kind == "need" and state["need"] >= self.max_need:
            return False
        state["players"].add(player)
        if kind == "need":
            state["need"] += 1
        candidate = (_KIND_RANK[kind], value, player)
        best = state["best"]
        if best is None or self._beats(candidate, best):
            state["best"] = candidate
        self.scanned += 1
        return True

    @staticmethod
    def _beats(candidate, best):
        cand_rank, cand_value, cand_player = candidate
        best_rank, best_value, best_player = best
        if cand_rank != best_rank:
            return cand_rank > best_rank
        if cand_value != best_value:
            return cand_value > best_value
        return cand_player < best_player

    def winner(self, item):
        state = self._items.get(item)
        if state is None or state["best"] is None:
            return None
        self.scanned += 1
        return state["best"][2]

    def scanned_count(self):
        return self.scanned
