from pathlib import Path
import inspect
import re
from sudoq.solvers import strategies


def inject_available_strategies():
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

    readme = Path("README.md")
    content = readme.read_text()
    # Insert between markers
    updated = re.sub(
        r"<!-- START_INJECT_STRATEGIES_DOCUMENTATION -->.*<!-- END_INJECT_STRATEGIES_DOCUMENTATION -->",
        "<!-- START_INJECT_STRATEGIES_DOCUMENTATION -->\n"
        + "\n".join(docs)
        + "<!-- END_INJECT_STRATEGIES_DOCUMENTATION -->",
        content,
        flags=re.DOTALL,
    )
    readme.write_text(updated)


if __name__ == "__main__":
    inject_available_strategies()
