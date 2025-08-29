# rentwise_pro/main.py
from init_db import init_db, SessionLocal
from cli.property_menu import property_menu
from cli.tenant_menu import tenant_menu
from cli.lease_menu import lease_menu
from utils import pause

def main():
    session = SessionLocal()
    actions = {
        "1": ("Properties", property_menu),
        "2": ("Tenants", tenant_menu),
        "3": ("Leases & Payments", lease_menu),
        "0": ("Exit", None),
    }

    while True:
        print("\n=== RentWise Pro ===")
        for k, (label, _) in actions.items():
            print(f"{k}. {label}")
        choice = input("Choose: ").strip()

        if choice == "0":
            print("Goodbye!")
            break

        action = actions.get(choice)
        if not action:
            print("Invalid choice.")
            pause()
            continue

        try:
            action[1](session)
        except Exception as e:
            print(f"❌ Error running '{action[0]}': {e}")
            import traceback; traceback.print_exc()
            pause()

    session.close()

if __name__ == "__main__":
    init_db()  # Ensures DB is ready
    main()
