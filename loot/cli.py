"""命令行入口：跑需求分配样例。"""

import argparse

from .core import Rolls


def main(argv=None):
    parser = argparse.ArgumentParser(prog="need-greed", description="需求分配")
    parser.add_argument("--sample", default="need", help="need / tie / dup / scan")
    args = parser.parse_args(argv)
    if args.sample == "need":
        rolls = Rolls(max_need=2)
        rolls.roll("p1", "sword", "greed", 90, 0)
        rolls.roll("p2", "sword", "need", 10, 10)
        print("winner=%s" % rolls.winner("sword"))
    elif args.sample == "tie":
        rolls = Rolls(max_need=2)
        rolls.roll("bob", "sword", "greed", 50, 0)
        rolls.roll("amy", "sword", "greed", 50, 10)
        print("winner=%s" % rolls.winner("sword"))
    elif args.sample == "dup":
        rolls = Rolls(max_need=2)
        rolls.roll("p1", "sword", "greed", 50, 0)
        print("second=%s" % str(rolls.roll("p1", "sword", "greed", 80, 10)).lower())
    elif args.sample == "scan":
        rolls = Rolls(max_need=100000)
        for index in range(3000):
            rolls.roll("p-%d" % index, "item-%d" % index, "greed", 50, index)
        for index in range(3000):
            rolls.winner("item-2999")
        print("scanned=%d" % rolls.scanned_count())
    else:
        raise SystemExit("需要 --sample need|tie|dup|scan")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
