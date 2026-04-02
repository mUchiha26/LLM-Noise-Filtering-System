# main.py (True Entry Point)
"""
🎓 Entry point: handles CLI args, loads config, calls orchestrator.
"""
import sys
from utils.config_loader import load_config
from pipeline import run_pipeline

def main():
    config = load_config()
    # Read from stdin or CLI args
    text = sys.stdin.read() if not sys.stdin.isatty() else sys.argv[1]
    results = run_pipeline(text, config)
    for r in results:
        print(r)

if __name__ == "__main__":
    main()