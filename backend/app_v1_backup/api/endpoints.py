from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
import shutil
from pathlib import Path
from uuid import uuid4
from datetime import datetime

from app.core.database import get_db
from app.models.all_models import Medicine, Prescription, Bill, BillItem, Pharmacist, InventoryTransaction, AuditLog
from app.schemas.schemas import ScanResponse, BillConfirmationRequest, MedicineResponse
from app.services.gemini_service import extract_medicines_from_prescription

router = APIRouter()

# --- Helpers ---
def generate_bill_number():
    # Simple bill number generation
    year = datetime.now().year
    count = uuid4().hex[:6].upper()
    return f"BILL-{year}-{count}"

def authenticate_pharmacist_by_pin(pin: str, db: Session):
    # In a real app, use bcrypt verify. For this demo, simple check or mock.
    # We will assume a simple PIN for now as per prompt "Simple PIN-based"
    # To make it work with the seed data, we'll implement a basic check.
    # Note: PINs should be hashed. We'll handle this in the seed data.
    # PIN: 1234
    print(f"DEBUG AUTH: Checking PIN: {pin}")
    pharmacist = db.query(Pharmacist).filter(Pharmacist.pin_hash == pin, Pharmacist.is_active == True).first()
    if pharmacist:
        print(f"DEBUG AUTH: Found Pharmacist: {pharmacist.name}")
    else:
        print("DEBUG AUTH: No pharmacist found with this PIN.")
    return pharmacist

# --- Endpoints ---

@router.post("/prescriptions/scan", response_model=ScanResponse)
async def scan_prescription(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1. Save uploaded image
    upload_dir = Path("uploads/prescriptions")
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / f"{uuid4()}.jpg"
    
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
        
    # 2. Call Gemini
    # Convert path to string for service
    extraction = await extract_medicines_from_prescription(str(file_path))
    
    # 3. Create prescription record
    prescription = Prescription(
        image_path=str(file_path),
        gemini_extraction_response=extraction,
        extraction_confidence=extraction.get("prescription_metadata", {}).get("overall_confidence", 0.0),
        is_readable=extraction.get("extraction_quality", {}).get("is_readable", False)
    )
    db.add(prescription)
    db.commit()
    db.refresh(prescription)
    
    # 4. Process medicines
    medicines_with_pricing = []
    bill_subtotal = 0.0
    
    extracted_medicines = extraction.get("medicines", [])
    
    for med_data in extracted_medicines:
        # fuzzy search or exact match? Prompt implies exact or close.
        # We'll try exact generic match first
        generic_name = med_data.get("generic_name", "").strip()
        medicine = db.query(Medicine).filter(
            Medicine.generic_name.ilike(generic_name)
        ).first()
        
        # Helper to construct item dict
        item = med_data.copy()
        item["found_in_inventory"] = False
        item["stock_available"] = False
        item["unit_price"] = 0.0
        item["line_total"] = 0.0
        item["gst_amount"] = 0.0
        item["item_total"] = 0.0
        item["current_stock"] = 0
        
        qty = int(med_data.get("quantity_prescribed") or 0)
        item["quantity_prescribed"] = qty # Fix Pydantic error by ensuring this is int, not None

        if medicine:
            item["medicine_id"] = medicine.id
            item["found_in_inventory"] = True
            item["current_stock"] = medicine.current_stock
            item["stock_available"] = medicine.current_stock >= qty
            item["unit_price"] = float(medicine.unit_price)
            
            line_total = float(medicine.unit_price) * qty
            gst_amount = line_total * (float(medicine.gst_rate) / 100.0)
            
            item["line_total"] = line_total
            item["gst_amount"] = gst_amount
            item["item_total"] = line_total + gst_amount
            
            bill_subtotal += line_total
        
        medicines_with_pricing.append(item)
        
    # 5. Totals
    total_gst = sum(m["gst_amount"] for m in medicines_with_pricing)
    final_amount = bill_subtotal + total_gst
    
    # 6. Create Bill (Pending)
    bill = Bill(
        bill_number=generate_bill_number(),
        prescription_id=prescription.id,
        patient_name=extraction.get("prescription_metadata", {}).get("patient_name"),
        patient_age=extraction.get("prescription_metadata", {}).get("patient_age"),
        subtotal=bill_subtotal,
        total_gst=total_gst,
        final_amount=final_amount,
        status="PENDING"
    )
    db.add(bill)
    db.commit()
    db.refresh(bill)
    
    # 7. Create Items (only for found ones? or all? Prompt says "Flag extractions... for manual review")
    # We will save all, but non-inventory ones might fail FK constraints if we enforce medicine_id.
    # The requirement says "Medicine not in database - flag for manual entry".
    # Since our DB schema forces medicine_id, we can't save non-existent medicines to bill_items yet.
    # In a real app we'd have a temporary items table or allow null medicine_id.
    # For this build, we will only save FOUND items to the DB, but return ALL to the UI.
    # The UI will likely need to "Add to Inventory" or map to existing before confirming.
    
    for m in medicines_with_pricing:
        if m["found_in_inventory"]:
             bill_item = BillItem(
                bill_id=bill.id,
                medicine_id=m["medicine_id"],
                quantity=m["quantity_prescribed"],
                unit_price=m["unit_price"],
                line_total=m["line_total"],
                gst_amount=m["gst_amount"],
                item_total=m["item_total"],
                dosage_frequency=m.get("frequency"),
                dosage_duration=m.get("duration"),
            )
             db.add(bill_item)
    db.commit()
    
    return {
        "status": "PENDING_CONFIRMATION",
        "bill_id": bill.id,
        "bill_number": bill.bill_number,
        "extraction_confidence": float(prescription.extraction_confidence or 0),
        "medicines": medicines_with_pricing,
        "subtotal": bill_subtotal,
        "total_gst": total_gst,
        "final_amount": final_amount,
        "warnings": [m for m in medicines_with_pricing if not m["found_in_inventory"] or not m["stock_available"]]
    }

@router.post("/bills/{bill_id}/confirm")
async def confirm_bill(
    bill_id: str,
    request: BillConfirmationRequest,
    db: Session = Depends(get_db)
):
    pharmacist = authenticate_pharmacist_by_pin(request.pharmacist_pin, db)
    if not pharmacist:
        raise HTTPException(status_code=401, detail="Invalid Pharmacist PIN")
        
    bill = db.query(Bill).filter(Bill.id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
        
    if bill.status != "PENDING":
        raise HTTPException(status_code=400, detail="Bill already processed")
        
    # Verify stock again
    items = db.query(BillItem).filter(BillItem.bill_id == bill_id).all()
    for item in items:
        med = db.query(Medicine).filter(Medicine.id == item.medicine_id).first()
        if med.current_stock < item.quantity:
             raise HTTPException(status_code=400, detail=f"Insufficient stock for {med.generic_name}")
             
    # Process
    bill.status = "CONFIRMED"
    bill.confirmed_by = pharmacist.id
    bill.confirmation_notes = request.notes
    
    for item in items:
        med = db.query(Medicine).filter(Medicine.id == item.medicine_id).first()
        
        # Transaction
        tx = InventoryTransaction(
            medicine_id=med.id,
            transaction_type="DISPENSED",
            quantity_change=-item.quantity,
            stock_before=med.current_stock,
            stock_after=med.current_stock - item.quantity,
            bill_id=bill.id,
            performed_by=pharmacist.id
        )
        db.add(tx)
        
        # Update stock
        med.current_stock -= item.quantity
        
    # Audit
    audit = AuditLog(
        pharmacist_id=pharmacist.id,
        action="BILL_CONFIRMED",
        resource_type="BILL",
        resource_id=bill.id,
        changes={"status": "CONFIRMED"}
    )
    db.add(audit)
    
    db.commit()
    
    return {"status": "success", "bill_number": bill.bill_number}

@router.get("/inventory", response_model=dict)
def get_inventory(
    search: Optional[str] = None, 
    low_stock_only: bool = False,
    db: Session = Depends(get_db)
):
    query = db.query(Medicine)
    
    if low_stock_only:
        query = query.filter(Medicine.current_stock < Medicine.min_stock_level)
        
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Medicine.generic_name.ilike(search_term),
                Medicine.brand_names.any(search) # Array contains
            )
        )
        
    medicines = query.all()
    
    res_list = []
    for m in medicines:
        res_list.append({
            "id": m.id,
            "generic_name": m.generic_name,
            "brand_names": m.brand_names,
            "strength": m.strength,
            "current_stock": m.current_stock,
            "min_stock_level": m.min_stock_level,
            "unit_price": float(m.unit_price),
            "stock_status": "LOW" if m.current_stock < m.min_stock_level else "OK"
        })
        
    return {"medicines": res_list}
