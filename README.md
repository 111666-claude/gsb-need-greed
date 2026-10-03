# need-greed

需求分配：需求优先、掷点比较、平局按名字、每人一票与需求票上限，只用 Python 标准库。

```
python3 -m loot.cli --sample need
python3 -m loot.cli --sample tie
python3 -m loot.cli --sample dup
python3 -m loot.cli --sample scan
python3 -m unittest discover -s tests -v
```

## 口径（README 为准）

- **需求优先**：`need` 的票一定压过 `greed` 的票，不看点数大小。
- **点数比较**：同为 `need` 或同为 `greed` 时点数大的赢。
- **平局**：点数相同按玩家 id 升序。
- **每人一票**：同一玩家对同一件物品只能投一次，重复投票返回 false。
- **需求票上限**：一件物品最多 `max_need` 张需求票，超出返回 false。
- **不变量**：结果只由已记录的票决定；同一串投票序列重复执行结果相同。
- **代价**：`winner` 不许扫描全部历史投票，`scanned_count` 不随投票数线性增长。
- **规模**：10 万张票、每秒 10 万次判定，单次摊还 O(该物品的票数)。

## 输出契约（不改格式）

```
winner=..
second=..
scanned=..
```

## 目录

```
loot/core.py   需求优先、掷点、平局与一票制
loot/cli.py    命令行入口
tests/         unittest 用例
```
