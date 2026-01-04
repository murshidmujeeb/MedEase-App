export interface Medicine {
    id?: string;
    generic_name: string;
    brand_names?: string[];
    strength: string;
    form: string;
    unit_price: number;
    current_stock: number;
    min_stock_level: number;
    stock_status?: string;
}

export interface BillItem {
    medicine_id: string;
    generic_name: string;
    strength: string;
    quantity_prescribed: number;
    unit_price: number;
    line_total: number;
    gst_amount: number;
    item_total: number;
    found_in_inventory: boolean;
    stock_available: boolean;
    frequency?: string;
    duration?: string;
}

export interface ClinicalAnalysis {
    inferred_diagnosis?: string;
    patient_advice?: string;
    pharmacist_notes?: string;
}

export interface ScanResponse {
    status: string;
    bill_id: string;
    bill_number: string;
    medicines: BillItem[];
    subtotal: number;
    total_gst: number;
    final_amount: number;
    extraction_confidence: number;
    doctor_notes?: string;
    clinical_analysis?: ClinicalAnalysis;
    warnings: any[];
}
