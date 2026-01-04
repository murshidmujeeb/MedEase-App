from app.core.database import SessionLocal
from app.models.all_models import Pharmacist

def create_admin():
    db = SessionLocal()
    try:
        print("Checking for Admin Pharmacist...")
        admin = db.query(Pharmacist).filter(Pharmacist.pin_hash == "1234").first()
        
        if admin:
            print(f"Admin already exists: {admin.name} (ID: {admin.id})")
        else:
            print("Admin not found. Creating now...")
            new_admin = Pharmacist(
                name="Admin Pharmacist",
                license_number="PHARM-001",
                pin_hash="1234",
                is_active=True
            )
            db.add(new_admin)
            db.commit()
            print("SUCCESS: Created Admin Pharmacist with PIN 1234")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
