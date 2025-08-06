import os
import questionary

def select_dump_file(dump_dir: str, extension=".dump") -> str | None:
    if not os.path.isdir(dump_dir):
        print(f"\u274c No such directory: {dump_dir}")
        return None

    files = [f for f in os.listdir(dump_dir) if f.endswith(extension)]
    if not files:
        print(f"\u274c No '{extension}' files found in {dump_dir}")
        return None

    selected = questionary.select("Select a dump file: ", choices=sorted(files)).ask()
    if not selected:
        return None

    return os.path.join(dump_dir, selected)