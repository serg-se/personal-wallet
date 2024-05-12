from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = MODULE_DIR.parents[1]
DEFAULT_CFG = PROJECT_DIR / "config.ini"
