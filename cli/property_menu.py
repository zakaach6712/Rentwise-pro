# cli/property_menu.py
from models.property import Property
from utils import input_int, input_str, pause
import traceback

def list_properties(session):
    props = Property.get_all(session)
    if not props:
        print("No properties found.")
    else:
        for p in props:
            print(p)
    pause()

def create_property(session):
    try:
        address = input_str("Address: ").strip()
        rent = input_int("Monthly rent: ", min_val=1)
        ptype = (input_str(
            "Property type (apartment/house/shop) [default apartment]: ",
            allow_empty=True
        ) or "apartment").strip()

        prop = Property.create(
            session,
            address=address,
            monthly_rent=rent,
            property_type=ptype
        )
        print(f"✅ Created {prop}")
    except Exception as e:
        session.rollback()
        print("❌ Error creating property.")
        traceback.print_exc()
    pause()

def delete_property(session):
    try:
        pid = input_int("Property ID to delete: ", min_val=1)
        prop = Property.find_by_id(session, pid)
        if not prop:
            print("Property not found.")
        else:
            if getattr(prop, "leases", []):
                print("⚠️  Warning: Property has related leases. Deleting will remove them.")
                confirm = input_str("Type 'DELETE' to confirm: ").strip()
                if confirm != "DELETE":
                    print("Cancelled.")
                    pause()
                    return
            prop.delete(session)
            print("✅ Deleted.")
    except Exception as e:
        session.rollback()
        print("❌ Error deleting property.")
        traceback.print_exc()
    pause()

def view_property_leases(session):
    pid = input_int("Property ID: ", min_val=1)
    prop = Property.find_by_id(session, pid)
    if not prop:
        print("Property not found.")
    else:
        leases = getattr(prop, "leases", [])
        if not leases:
            print("No leases for this property.")
        else:
            for l in leases:
                print(l)
    pause()

def find_property_by_attribute(session):
    field = input_str("Search by (address/property_type/is_available): ").strip()
    value = input_str("Value: ").strip()
    if field == "is_available":
        value = value.lower() in ("1", "true", "yes", "y")

    results = Property.find_by_attribute(session, **{field: value})
    if not results:
        print("No matches found.")
    else:
        for r in results:
            print(r)
    pause()

def property_menu(session):
    actions = {
        "1": ("List all properties", list_properties),
        "2": ("Create property", create_property),
        "3": ("Delete property", delete_property),
        "4": ("View a property's leases", view_property_leases),
        "5": ("Find property by attribute", find_property_by_attribute),
        "0": ("Back", None),
    }

    while True:
        print("\n=== Property Menu ===")
        for k, (label, _) in actions.items():
            print(f"{k}. {label}")
        choice = input("Choose: ").strip()

        if choice == "0":
            break
        action = actions.get(choice)
        if not action:
            print("Invalid choice. Please enter one of the listed numbers.")
            continue

        try:
            action[1](session)
        except Exception as e:
            print(f"❌ Error running '{action[0]}' action.")
            traceback.print_exc()
            pause()
