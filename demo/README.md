# Demo And Comparison Apps

Files in this directory are local developer/demo utilities. They are not part
of the published `uncommon_route` runtime API.

The comparison UI backend lives in [compare_api.py](compare_api.py).

Run it with either of these commands from the repo root:

```bash
python -m demo.compare_api
```

```bash
uvicorn demo.compare_api:app --reload --port 3721
```

The root-level [api.py](../api.py) is now only a compatibility shim so older local commands do not break.
