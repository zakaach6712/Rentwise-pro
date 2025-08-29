# utils.py
def input_str(prompt: str, allow_empty: bool = False) -> str:
    while True:
        val = input(prompt)
        if allow_empty and val.strip() == "":
            return ""
        if val.strip():
            return val.strip()
        print("Input cannot be empty.")

def input_int(prompt: str, min_val: int | None = None, max_val: int | None = None) -> int:
    while True:
        raw = input(prompt).strip()
        if not raw:
            print("Input cannot be empty.")
            continue
        if not raw.lstrip("-").isdigit():
            print("Enter a valid integer.")
            continue
        val = int(raw)
        if min_val is not None and val < min_val:
            print(f"Value must be >= {min_val}.")
            continue
        if max_val is not None and val > max_val:
            print(f"Value must be <= {max_val}.")
            continue
        return val

def pause():
    input("\nPress Enter to continue...")
