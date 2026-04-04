import importlib

libraries = [
    "numpy", 
    "pandas", 
    "matplotlib", 
    "sklearn", 
    "tensorflow", 
    "hdbscan"
]

print("--- Library Check ---")
for lib in libraries:
    try:
        __import__(lib)
        print(f"✅ {lib} is installed.")
    except ImportError:
        print(f"❌ {lib} is MISSING.")

print("\nIf all are checked, your code will run!")