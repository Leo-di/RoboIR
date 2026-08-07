# Contributing

Thanks for helping improve RoboIR.

## Before you start

- install the project in editable mode: `python -m pip install -e .[dev]`
- run the test suite: `pytest`
- keep changes small and focused on one extension seam when possible

## Good contribution targets

- new task packs under `src/roboir/tasks/`
- new adapters under `src/roboir/adapters/`
- new plugins under `src/roboir_plugins/`
- new docs or examples that make the framework easier to try

## Style

- prefer clear names over clever shortcuts
- keep public APIs stable when possible
- add or update tests when behavior changes
- update the README or docs if the user flow changes

## Suggested workflow

1. reproduce the behavior locally
2. make the smallest useful change
3. run the relevant tests
4. update docs or examples if needed
5. open a focused pull request
