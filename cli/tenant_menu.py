# cli/tenant_menu.py
from models.tenant import Tenant
from utils import input_int, input_str, pause
import traceback

def list_tenants(session):
    tenants = Tenant.get_all(session)
    if not tenants:
        print("No tenants found.")
    else:
        for t in tenants:
            print(t)
    pause()

def create_tenant(session):
    try:
        name = input_str("Name: ").strip()
        contact = input_str("Contact info: ").strip()
        t = Tenant.create(session, name=name, contact_info=contact)
        print(f"✅ Created {t}")
    except Exception as e:
        session.rollback()
        print("❌ Error creating tenant.")
        traceback.print_exc()
    pause()

def delete_tenant(session):
    try:
        tid = input_int("Tenant ID to delete: ", min_val=1)
        t = Tenant.find_by_id(session, tid)
        if not t:
            print("Tenant not found.")
        else:
            if getattr(t, "leases", []):
                print("⚠️  Warning: Tenant has related leases. Deleting will remove them.")
                confirm = input_str("Type 'DELETE' to confirm: ").strip()
                if confirm != "DELETE":
                    print("Cancelled.")
                    pause()
                    return
            t.delete(session)
            print("✅ Deleted.")
    except Exception as e:
        session.rollback()
        print("❌ Error deleting tenant.")
        traceback.print_exc()
    pause()

def view_tenant_leases(session):
    tid = input_int("Tenant ID: ", min_val=1)
    t = Tenant.find_by_id(session, tid)
    if not t:
        print("Tenant not found.")
    else:
        leases = getattr(t, "leases", [])
        if not leases:
            print("No leases for this tenant.")
        else:
            for l in leases:
                print(l)
    pause()

def find_tenant_by_attribute(session):
    field = input_str("Search by (name/contact_info): ").strip()
    value = input_str("Value: ").strip()
    results = Tenant.find_by_attribute(session, **{field: value})
    if not results:
        print("No matches found.")
    else:
        for r in results:
            print(r)
    pause()

def tenant_menu(session):
    actions = {
        "1": ("List all tenants", list_tenants),
        "2": ("Create tenant", create_tenant),
        "3": ("Delete tenant", delete_tenant),
        "4": ("View a tenant's leases", view_tenant_leases),
        "5": ("Find tenant by attribute", find_tenant_by_attribute),
        "0": ("Back", None),
    }

    while True:
        print("\n=== Tenant Menu ===")
        for k, (label, _) in actions.items():
            print(f"{k}. {label}")
        choice = input("Choose: ").strip()

        if choice == "0":
            break
        action = actions.get(choice)
        if not action:
            print("Invalid choice. Please try again.")
            pause()
            continue

        try:
            action[1](session)
        except Exception as e:
            print(f"❌ Error running '{action[0]}' action.")
            traceback.print_exc()
            pause()
