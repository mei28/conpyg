# **conpyg**

*A lightweight, dependency‑minimal configuration helper for Python projects*

---

![PyPI](https://img.shields.io/pypi/v/conpyg?color=brightgreen)
![License](https://img.shields.io/github/license/mei28/conpyg)

`conpyg` lets you **load**, **update**, and **save** deeply‑nested configuration trees from YAML / JSON files and override any key from the command line:

```console
$ python main.py --config config/base.yaml --set training.lr=0.0001 --set debug=true
```

---

## ✨ Features

| Feature                    | Details                                                                             |
| -------------------------- | ----------------------------------------------------------------------------------- |
| 🔄 **Deep merge**          | Layer any number of dicts/configs; lower layers override higher layers recursively. |
| ⚡ **Dot‑notation access**  | `cfg.database.host` / `cfg["database.host"]` – whichever you prefer.                |
| 🛠️ **CLI overrides**      | `--set key=value` converts to bool / int / float / str automatically.               |
| 💾 **Easy I/O**            | `Config.load()` / `.save()` support **YAML** & **JSON** out of the box.             |
| 🧪 **100 % test coverage** | Property‑based tests (Hypothesis) ensure merge idempotency & more.                  |
| ⚖️ **Zero heavy deps**     | Only runtime dependency is `PyYAML`.                                                |

---

## 📦 Installation

### 🔔 Latest release from PyPI (pip)

```bash
pip install conpyg             # fresh install
pip install -U conpyg          # upgrade to newest version
```

### 🚀 Local development clone (uv editable)

```bash
# clone the repository first
git clone https://github.com/yourname/conpyg.git
cd conpyg

uv pip install -e .            # installs in editable mode
```

> \*\*Tip \*\*: `uv` is a drop‑in replacement for pip + virtualenv that creates an isolated environment automatically. You can of course use the standard combo:
>
> ```bash
> python -m venv .venv && source .venv/bin/activate
> pip install -e .[dev]
> ```

---

## 🚀 Quick‑start

```python
from conpyg import Config

cfg = Config.load("config/default.yaml")            # → nested settings
print(cfg.db.host)                                   # dot access
print(cfg["db.port"])                               # bracket access

cfg["api.timeout"] = 30                             # mutate in‑memory
cfg.merge({"feature_flags": {"beta": True}})       # deep merge override

cfg.save("run_config_snapshot.yaml")                # persist
```

### CLI helper

```python
# main.py
auth_cfg = Config.from_cli()   # --config & --set are parsed automatically
```

Run:

```console
python main.py \
  --config config/prod.yaml \
  --set log.level=warning --set retries=5
```

---

## 🧪 Running the test‑suite

```bash
uv run pytest -q --cov=conpyg --cov-report=term-missing
```

All core paths are covered; property tests guard against regressions in the merge logic.

---

## 🔧 Development workflow (with **uv**)

| Task                   | Command                            |
| ---------------------- | ---------------------------------- |
| **Install dev deps**   | `uv sync --dev`                    |
| **Add a dependency**   | `uv add PyYAML`                    |
| **Add a dev‑only dep** | `uv add --dev pytest`              |
| **Lock updates**       | `uv lock`                          |
| **Build distribution** | `uv build`                         |
| **Publish (TestPyPI)** | `uv publish --repository testpypi` |

---

## 📄 License

`conpyg` is released under the MIT License – see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

Inspired by the simplicity of [OmegaConf](https://omegaconf.readthedocs.io/) & the stability of [Hydra](https://hydra.cc/), but crafted to stay tiny and dependency‑free.

