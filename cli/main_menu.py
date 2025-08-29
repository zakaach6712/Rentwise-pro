# cli/main_menu.py
from cli.property_menu import property_menu
from cli.tenant_menu import tenant_menu
from cli.lease_menu import lease_menu
from utils import pause  # to give user time to read errors

def main_menu(session):
    actions = {
        "1": ("Properties", property_menu),
        "2": ("Tenants", tenant_menu),
        "3": ("Leases & Payments", lease_menu),
        "0": ("Exit", None),
    }

    while True:
        print("\n" + "=" * 30)
        print("       RentWise Pro CLI")
        print("=" * 30)
        for key, (label, _) in actions.items():
            print(f"{key}. {label}")
        print("h. Help (show this menu again)")

        choice = input("Choose: ").strip().lower()

        if choice == "0":
            print("Goodbye!")
            break
        if choice == "h" or choice == "":
            # loop back and show menu again
            continue

        action = actions.get(choice)
        if not action:
            print("Invalid choice. Enter a listed number or 'h' for help.")
            pause()
            continue

        try:
            action[1](session)
        except Exception as e:
            import traceback
            print(f"\n❌ An error occurred while running '{action[0]}': {e}")
            traceback.print_exc()
            pause()
