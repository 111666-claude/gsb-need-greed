"""需求分配：需求优先、掷点比较、平局按名字、每人一票与需求票上限。

缺陷：不区分需求与贪婪、平局看先来后到、同一人可重复投票、
需求票上限不生效、每次判定扫描全部投票。
"""


class Rolls:
    def __init__(self, max_need):
        self.max_need = max_need
        self.entries = []
        self.scanned = 0

    def roll(self, player, item, kind, value, at_ms):
        self.scanned += len(self.entries)
        self.entries.append((player, item, kind, value, at_ms))
        return True

    def winner(self, item):
        self.scanned += len(self.entries)
        best = None
        for player, it, kind, value, _ in self.entries:
            if it != item:
                continue
            if best is None or value > best[1]:
                best = (player, value)
        return None if best is None else best[0]

    def scanned_count(self):
        return self.scanned
