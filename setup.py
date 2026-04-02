import sys
from pipeline import run_pipeline

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        text = f.read()

    results = run_pipeline(text)

    print("\n=== RELEVANT CONTENT ===\n")
    for r in results:
        print("-", r)
