import os
import sys
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from core import jaro_link_agent


TEST_LOG_FILE = os.path.join(os.path.dirname(__file__), "agent_test_log.json")


def _setup_logging():
    """Reroute logging to a test file to avoid production logs."""
    jaro_link_agent.LOG_FILE = TEST_LOG_FILE
    if os.path.exists(TEST_LOG_FILE):
        os.remove(TEST_LOG_FILE)


def test_init_agent():
    """Initialiseer JaroLinkAgent en toon profielinformatie."""
    start = time.perf_counter()
    try:
        agent = jaro_link_agent.JaroLinkAgent()
    except Exception as exc:
        duration = time.perf_counter() - start
        print(f"Fout bij initialisatie: {exc}")
        print(f"Laadtijd: {duration:.2f}s")
        return None
    duration = time.perf_counter() - start
    active = agent.profile.get("actieve_modules", agent.profile.get("modules", []))
    print(f"Profielstatus: {agent.status}")
    print(f"Aantal actieve modules: {len(active)}")
    print(f"Laadtijd: {duration:.2f}s")
    return agent


def test_module_activation(agent):
    """Voer agent.run() uit en controleer ingeladen modules."""
    start = time.perf_counter()
    try:
        agent.run()
    except Exception as exc:
        duration = time.perf_counter() - start
        print(f"Fout tijdens run: {exc}")
        print(f"Laadtijd: {duration:.2f}s")
        return False
    duration = time.perf_counter() - start
    print(f"Aantal geladen modules: {len(agent.modules)}")
    print(f"Laadtijd: {duration:.2f}s")
    print("Test succesvol uitgevoerd")
    return True


def main():
    _setup_logging()
    agent = test_init_agent()
    if agent:
        test_module_activation(agent)


if __name__ == "__main__":
    main()
