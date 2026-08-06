from roboir.tasks import build_task_pack


def main() -> None:
    pack = build_task_pack("lab")
    report = pack.benchmark.run(pack.runtime)
    print(report.summary())


if __name__ == "__main__":
    main()
