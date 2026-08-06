from roboir.tasks import build_workcell_pack


def main() -> None:
    pack = build_workcell_pack()
    report = pack.benchmark.run(pack.runtime)
    print(report.summary())


if __name__ == "__main__":
    main()
