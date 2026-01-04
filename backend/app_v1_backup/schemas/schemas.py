from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

# Bill/Prescription Schemas
class MedicineExtraction(BaseModel):
    generic_name: str
    brand_name: Optional[str] = None
    strength: str
    form: str
    quantity_prescribed: int
    frequency: Optional[str] = None
    duration: Optional[str] = None
    special_instructions: Optional[str] = None
    extraction_confidence: float

class PrescriptionMetadata(BaseModel):
    patient_name: Optional[str] = None
    patient_age: Optional[int] = None
    prescriber_name: Optional[str] = None
    prescription_date: Optional[str] = None
    overall_confidence: Optional[float] = None

class ExtractionQuality(BaseModel):
    is_readable: bool
    missing_fields: List[str] = []
    overall_suggestion: Optional[str] = None
    error: Optional[str] = None

class GeminiResponse(BaseModel):
    prescription_metadata: PrescriptionMetadata
    medicines: List[MedicineExtraction]
    extraction_quality: ExtractionQuality

# API Response Schemas
class MedicinePriceCheck(MedicineExtraction):
    medicine_id: Optional[str] = None
    found_in_inventory: bool
    unit_price: Optional[float] = None
    line_total: Optional[float] = None
    gst_amount: Optional[float] = None
    item_total: Optional[float] = None
    stock_available: bool = False
    current_stock: int = 0

class ScanResponse(BaseModel):
    status: str
    bill_id: str
    bill_number: str
    extraction_confidence: float
    medicines: List[MedicinePriceCheck]
    subtotal: float
    total_gst: float
    final_amount: float
    warnings: List[dict]

class BillConfirmationRequest(BaseModel):
    pharmacist_pin: str
    notes: Optional[str] = None

class MedicineResponse(BaseModel):
    id: str
    generic_name: str
    brand_names: Optional[List[str]] = []
    strength: str
    current_stock: int
    min_stock_level: int
    unit_price: float
    stock_status: str
