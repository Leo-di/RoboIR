# RoboIR

RoboIR is a modular embodied orchestration layer for desk-level industrial and service robotics.

## What it is

RoboIR sits between perception, planning, execution, recovery, memory, and human intervention.

## Start here

```bash
roboir run --pack deskservice --adapter mock
roboir browse
roboir examples
roboir templates
```

## Best first paths

- [`Getting Started`](GETTING_STARTED.md)
- [`Portal`](PORTAL.md)
- [`Examples`](EXAMPLES.md)
- [`Architecture`](ARCHITECTURE.md)
- [`Extending`](EXTENDING.md)

## Why this repo is different

Most embodied-AI repos are centered on a model or benchmark.
RoboIR is centered on reuse:

- task packs for scenario packaging
- plugins for reusable skills and affordances
- adapters for backend surfaces
- traces for evaluation and reuse
