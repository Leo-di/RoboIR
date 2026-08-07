# RoboIR Portal

The portal is the unified landing page for people exploring RoboIR for the first time.

## Why it matters

High-star robotics repos usually do three things well:

- keep the homepage short
- point to the first useful command immediately
- show a clean extension surface

RoboIR follows that pattern with a single portal for discovery.

## Sections

- Examples — runnable scripts for demos, orchestration, and benchmarks
- Templates — copyable skeletons for downstream extensions
- Adapters — supported execution backends and runtime surfaces
- Task Packs — built-in task bundles for different embodied domains
- Plugins — discoverable skill and affordance bundles

## Commands

```bash
roboir browse
roboir browse --section Examples
roboir browse --section Templates
roboir examples
roboir templates
roboir adapters
```

## Recommended path

1. run `roboir run --pack deskservice --adapter mock`
2. open `roboir browse`
3. copy a template into a downstream package
4. extend with your own skills, adapters, or task packs
