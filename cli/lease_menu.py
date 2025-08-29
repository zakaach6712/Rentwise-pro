# cli/lease_menu.py
from datetime import datetime, date
from models.lease import Lease
from models.property import Property
from models.tenant import Tenant
from models.payment import Payment
from utils import input_int, input_str, pause

def parse_date(prompt: str) -> date:
    while True:
        raw = input_str(f"{prompt} (YYYY-MM-DD): ").strip()
        try:
            return datetime.strptime(raw, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")

def list_leases(session):
    leases = Lease.get_all(session)
    if not leases:
        print("No leases found.")
    else:
        for l in leases:
            print(l)
    pause()

def create_lease(session):
    try:
        pid = input_int("Property ID: ", min_val=1)
        tid = input_int("Tenant ID: ", min_val=1)
        start = parse_date("Start date")
        status = (input_str("Status [active/ended] (default active): ", allow_empty=True) or "active").strip()

        prop = Property.find_by_id(session, pid)
        tenant = Tenant.find_by_id(session, tid)
        if not prop:
            print("Property not found.")
            pause()
            return
        if not tenant:
            print("Tenant not found.")
            pause()
            return

        lease = Lease.create(session, property_id=pid, tenant_id=tid, start_date=start, status=status)
        print(f"Created {lease}")
    except Exception as e:
        session.rollback()
        import traceback; traceback.print_exc()
        print(f"Error: {e}")
    pause()

def end_lease(session):
    lid = input_int("Lease ID to end: ", min_val=1)
    lease = Lease.find_by_id(session, lid)
    if not lease:
        print("Lease not found.")
        pause()
        return
    if lease.status == "ended":
        print("Lease already ended.")
        pause()
        return
    end = parse_date("End date")
    try:
        lease.end(session, end)
        print("Lease ended.")
    except Exception as e:
        session.rollback()
        import traceback; traceback.print_exc()
        print(f"Error: {e}")
    pause()

def delete_lease(session):
    lid = input_int("Lease ID to delete: ", min_val=1)
    lease = Lease.find_by_id(session, lid)
    if not lease:
        print("Lease not found.")
    else:
        if getattr(lease, "payments", []):
            print("Warning: Lease has related payments. Deleting will remove them.")
            confirm = input_str("Type 'DELETE' to confirm: ").strip()
            if confirm != "DELETE":
                print("Cancelled.")
                pause()
                return
        lease.delete(session)
        print("Deleted.")
    pause()

def find_lease_by_attribute(session):
    field = input_str("Search by (status/property_id/tenant_id): ").strip()
    value_raw = input_str("Value: ").strip()
    value = int(value_raw) if field in ("property_id", "tenant_id") else value_raw
    results = Lease.find_by_attribute(session, **{field: value})
    if not results:
        print("No matches.")
    else:
        for r in results:
            print(r)
    pause()

# ----- Payment operations -----

def list_payments_for_lease(session):
    lid = input_int("Lease ID: ", min_val=1)
    lease = Lease.find_by_id(session, lid)
    if not lease:
        print("Lease not found.")
        pause()
        return
    if not getattr(lease, "payments", []):
        print("No payments recorded for this lease.")
    else:
        for p in lease.payments:
            print(p)
    pause()

def create_payment(session):
    try:
        lid = input_int("Lease ID: ", min_val=1)
        lease = Lease.find_by_id(session, lid)
        if not lease:
            print("Lease not found.")
            pause()
            return
        amount_str = input_str("Amount (e.g., 15000 or 15000.00): ").strip()
        try:
            amount = float(amount_str)
        except ValueError:
            print("Invalid amount.")
            pause()
            return
        paid_on = parse_date("Date paid")
        method = (input_str("Method [cash/mpesa/bank]: ", allow_empty=True) or "cash").strip()
        pay = Payment.create(session, lease_id=lid, amount=amount, date_paid=paid_on, method=method)
        print(f"Created {pay}")
    except Exception as e:
        session.rollback()
        import traceback; traceback.print_exc()
        print(f"Error: {e}")
    pause()

def delete_payment(session):
    pid = input_int("Payment ID to delete: ", min_val=1)
    pay = Payment.find_by_id(session, pid)
    if not pay:
        print("Payment not found.")
    else:
        pay.delete(session)
        print("Deleted.")
    pause()

def find_payment_by_attribute(session):
    field = input_str("Search payment by (method/lease_id): ").strip()
    value_raw = input_str("Value: ").strip()
    value = int(value_raw) if field == "lease_id" else value_raw
    results = Payment.find_by_attribute(session, **{field: value})
    if not results:
        print("No matches.")
    else:
        for r in results:
            print(r)
    pause()

def lease_menu(session):
    actions = {
        "1": ("List all leases", list_leases),
        "2": ("Create lease", create_lease),
        "3": ("End lease", end_lease),
        "4": ("Delete lease", delete_lease),
        "5": ("Find lease by attribute", find_lease_by_attribute),
        "6": ("List payments for a lease", list_payments_for_lease),
        "7": ("Create payment", create_payment),
        "8": ("Delete payment", delete_payment),
        "9": ("Find payment by attribute", find_payment_by_attribute),
        "0": ("Back", None),
    }
    while True:
        print("\n=== Lease & Payments Menu ===")
        for k, (label, _) in actions.items():
            print(f"{k}. {label}")
        choice = input("Choose: ").strip()
        if choice == "0":
            break
        action = actions.get(choice)
        if not action:
            print("Invalid choice.")
            continue
        action[1](session)
