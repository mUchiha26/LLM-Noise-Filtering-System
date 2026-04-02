import sys
import json
from utils.config_loader import load_config
from pipeline import run_pipeline

def main():
    config = load_config()
    text = sys.stdin.read().strip() if not sys.stdin.isatty() else " ".join(sys.argv[1:])
    if not text:
        print("Usage: echo 'text' | python main.py  OR  python main.py 'your text'", file=sys.stderr)
        sys.exit(1)
        
    results = run_pipeline(text, config)
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()