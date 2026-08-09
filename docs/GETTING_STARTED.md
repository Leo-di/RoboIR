# Getting Started

This guide is the fastest way to try RoboIR as a framework.

## Install

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .[dev]
```

## Try the deskservice pack

```bash
roboir run --pack deskservice --adapter mock
```

Expected output:

- a compact summary in the terminal
- a structured report when `--json` is provided
- trace, failure, and memory data inside the runtime

## Other useful commands

```bash
roboir catalog
roboir benchmark --pack deskservice
roboir suite --packs workcell lab office retail deskservice
roboir plugins
roboir scene --pack deskservice --output scene.json
roboir scene --input scene.json
roboir adapters
roboir report --pack deskservice --json report.json
roboir trace --pack deskservice --markdown trace.md
roboir visualize --pack deskservice --kind scene
roboir visualize --pack deskservice --kind trace
roboir templates
roboir examples
roboir browse
```

## What to extend first

If you want to build on RoboIR, start with one of these:

- a new task pack for a new embodied domain
- a new adapter for a simulator or robot backend
- a plugin that adds reusable skills and affordances
