import os
import warnings
import importlib.util

class ConfigWarning(Warning):
    pass

def test_dump_root_exists_or_warns():
    config_path = os.path.abspath("src/core/config.py")  # Adjust if needed
    spec = importlib.util.spec_from_file_location("config", config_path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)

    if not hasattr(config, "DUMP_ROOT"):
        message = "⚠ DUMP_ROOT is not set in config.py. Please configure it before running critical operations."
        print(f"\n\033[93m{message}\033[0m\n")  # Bright yellow print
        warnings.warn(message, ConfigWarning)
        return

    dump_root = config.DUMP_ROOT
    assert os.path.isdir(dump_root), f"❌ DUMP_ROOT is set to {dump_root}, but this directory does not exist."