from pathlib import Path
import inspect
import re
from sudoq.solvers import strategies


def inject_into_readme(marker: str, content: str):
    readme = Path("README.md")
    # Insert between markers
    start_marker = f"<!-- START_INJECT_{marker} -->"
    end_marker = f"<!-- END_INJECT_{marker} -->"
    updated = re.sub(
        rf"{start_marker}.*{end_marker}",
        f"{start_marker}\n" + content + f"{end_marker}",
        readme.read_text(),
        flags=re.DOTALL,
    )
    if updated:
        readme.write_text(updated)
        return True


def inject_code_examples():
    example_code = Path("examples", "solving.py").read_text()
    example_code = f"```python\n{example_code}\n```"
    return inject_into_readme(
        marker="CODE_EXAMPLE",
        content=example_code,
    )


def inject_strategies():
    strategy_classes = [
        cls
        for _, cls in inspect.getmembers(strategies, inspect.isclass)
        if issubclass(cls, strategies.SolvingStrategy)
        and cls != strategies.SolvingStrategy
    ]

    docs = []
    for strategy in strategy_classes:
        docs.append(f"### {strategy.__name__}")
        docs.append(f"{strategy.__doc__ or 'No description available.'}\n")

    return inject_into_readme(
        marker="STRATEGIES",
        content="\n".join(docs),
    )


if __name__ == "__main__":
    exit(0 if (inject_code_examples() and inject_strategies()) else 1)
