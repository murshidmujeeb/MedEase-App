
# Common medicines dataset for Indian Pharmacy Context
MEDICINES_DATA = [
    # --- Antibiotics ---
    {"generic_name": "Amoxicillin", "brand_names": ["Mox", "Novamox", "Amoxil"], "strength": "500 mg", "form": "Capsule", "unit_price": 10.00, "category": "Antibiotic"},
    {"generic_name": "Amoxicillin + Clavulanic Acid", "brand_names": ["Augmentin", "Clavam", "Moxikind-CV"], "strength": "625 mg", "form": "Tablet", "unit_price": 25.00, "category": "Antibiotic"},
    {"generic_name": "Azithromycin", "brand_names": ["Azithral", "Aje", "Zithromax"], "strength": "500 mg", "form": "Tablet", "unit_price": 22.00, "category": "Antibiotic"},
    {"generic_name": "Cefixime", "brand_names": ["Taxim-O", "Zifi", "Cefolac"], "strength": "200 mg", "form": "Tablet", "unit_price": 18.00, "category": "Antibiotic"},
    {"generic_name": "Cefpodoxime", "brand_names": ["Cepodem", "Monocef-O", "Doxcef"], "strength": "200 mg", "form": "Tablet", "unit_price": 28.00, "category": "Antibiotic"},
    {"generic_name": "Ciprofloxacin", "brand_names": ["Cifran", "Ciplox"], "strength": "500 mg", "form": "Tablet", "unit_price": 8.00, "category": "Antibiotic"},
    {"generic_name": "Levofloxacin", "brand_names": ["Levoflox", "Loxof", "Glevo"], "strength": "500 mg", "form": "Tablet", "unit_price": 12.00, "category": "Antibiotic"},
    {"generic_name": "Metronidazole", "brand_names": ["Flagyl", "Metrogyl"], "strength": "400 mg", "form": "Tablet", "unit_price": 2.00, "category": "Antibiotic"},
    {"generic_name": "Ofloxacin", "brand_names": ["Zanocin", "Oflox"], "strength": "200 mg", "form": "Tablet", "unit_price": 10.00, "category": "Antibiotic"},
    {"generic_name": "Doxycycline", "brand_names": ["Doxy-1", "Microdox"], "strength": "100 mg", "form": "Capsule", "unit_price": 5.00, "category": "Antibiotic"},

    # --- Analgesics / Antipyretics / Pain Management ---
    {"generic_name": "Paracetamol", "brand_names": ["Dolo 650", "Calpol", "Crocin"], "strength": "650 mg", "form": "Tablet", "unit_price": 2.50, "category": "Analgesic"},
    {"generic_name": "Ibuprofen", "brand_names": ["Brufen"], "strength": "400 mg", "form": "Tablet", "unit_price": 3.00, "category": "Analgesic"},
    {"generic_name": "Diclofenac Sodium", "brand_names": ["Voveran", "Reactin"], "strength": "50 mg", "form": "Tablet", "unit_price": 4.00, "category": "Analgesic"},
    {"generic_name": "Aceclofenac + Paracetamol", "brand_names": ["Zerodol-P", "Aceclo Plus"], "strength": "100mg/325mg", "form": "Tablet", "unit_price": 6.00, "category": "Analgesic"},
    {"generic_name": "Aceclofenac + Paracetamol + Serratiopeptidase", "brand_names": ["Acenext SP", "Zerodol-SP", "Signoflam"], "strength": "Standard", "form": "Tablet", "unit_price": 12.00, "category": "Analgesic"},
    {"generic_name": "Tramadol", "brand_names": ["Tramazac", "Ultracet"], "strength": "50 mg", "form": "Capsule", "unit_price": 15.00, "category": "Analgesic"},
    {"generic_name": "Etoricoxib", "brand_names": ["Nucoxia", "Etorica"], "strength": "90 mg", "form": "Tablet", "unit_price": 14.00, "category": "Analgesic"},
    {"generic_name": "Mefenamic Acid", "brand_names": ["Meftal-P", "Meftal Spas"], "strength": "500 mg", "form": "Tablet", "unit_price": 5.00, "category": "Analgesic"},

    # --- Antacids / PPIs / Gastric ---
    {"generic_name": "Pantoprazole", "brand_names": ["Pan", "Pan-40", "Pantocid"], "strength": "40 mg", "form": "Tablet", "unit_price": 9.00, "category": "Antacid"},
    {"generic_name": "Omeprazole", "brand_names": ["Omez", "Ocid"], "strength": "20 mg", "form": "Capsule", "unit_price": 6.00, "category": "Antacid"},
    {"generic_name": "Rabeprazole", "brand_names": ["Razo", "Rabicip"], "strength": "20 mg", "form": "Tablet", "unit_price": 11.00, "category": "Antacid"},
    {"generic_name": "Ranitidine", "brand_names": ["Rantac", "Aciloc"], "strength": "150 mg", "form": "Tablet", "unit_price": 2.00, "category": "Antacid"},
    {"generic_name": "Pantoprazole + Domperidone", "brand_names": ["Pan-D", "Pantocid-D"], "strength": "40mg/30mg", "form": "Capsule", "unit_price": 15.00, "category": "Antacid"},
    {"generic_name": "Esomeprazole", "brand_names": ["Nexpro", "Esoz"], "strength": "40 mg", "form": "Tablet", "unit_price": 12.00, "category": "Antacid"},
    {"generic_name": "Ondansetron", "brand_names": ["Emeset", "Vomitstop"], "strength": "4 mg", "form": "Tablet", "unit_price": 5.00, "category": "Antiemetic"},

    # --- Antidiabetics ---
    {"generic_name": "Metformin", "brand_names": ["Glycomet", "Gluconorm"], "strength": "500 mg", "form": "Tablet", "unit_price": 3.00, "category": "Antidiabetic"},
    {"generic_name": "Metformin SR", "brand_names": ["Glycomet-SR"], "strength": "1000 mg", "form": "Tablet", "unit_price": 5.00, "category": "Antidiabetic"},
    {"generic_name": "Glimepiride", "brand_names": ["Amaryl", "Glimestar"], "strength": "1 mg", "form": "Tablet", "unit_price": 6.00, "category": "Antidiabetic"},
    {"generic_name": "Glimepiride + Metformin", "brand_names": ["Gluconorm-G1", "Geminy M1"], "strength": "1mg/500mg", "form": "Tablet", "unit_price": 9.00, "category": "Antidiabetic"},
    {"generic_name": "Vildagliptin", "brand_names": ["Galvus", "Zomelis"], "strength": "50 mg", "form": "Tablet", "unit_price": 20.00, "category": "Antidiabetic"},
    {"generic_name": "Teneligliptin", "brand_names": ["Tenepure", "Dynaglipt"], "strength": "20 mg", "form": "Tablet", "unit_price": 15.00, "category": "Antidiabetic"},
    {"generic_name": "Dapagliflozin", "brand_names": ["Forxiga", "Dapanorm"], "strength": "10 mg", "form": "Tablet", "unit_price": 45.00, "category": "Antidiabetic"},

    # --- Antihypertensives (BP) / Cardiac ---
    {"generic_name": "Amlodipine", "brand_names": ["Amlong", "Stamlo"], "strength": "5 mg", "form": "Tablet", "unit_price": 4.00, "category": "Cardiac"},
    {"generic_name": "Telmisartan", "brand_names": ["Telma", "Telmikind"], "strength": "40 mg", "form": "Tablet", "unit_price": 8.00, "category": "Cardiac"},
    {"generic_name": "Telmisartan + Amlodipine", "brand_names": ["Telma-AM", "Telista-AM"], "strength": "40mg/5mg", "form": "Tablet", "unit_price": 12.00, "category": "Cardiac"},
    {"generic_name": "Losartan", "brand_names": ["Losar", "Repace"], "strength": "50 mg", "form": "Tablet", "unit_price": 7.00, "category": "Cardiac"},
    {"generic_name": "Enalapril", "brand_names": ["Envas"], "strength": "5 mg", "form": "Tablet", "unit_price": 3.00, "category": "Cardiac"},
    {"generic_name": "Atorvastatin", "brand_names": ["Atorva", "Lipikind"], "strength": "10 mg", "form": "Tablet", "unit_price": 10.00, "category": "Cardiac"},
    {"generic_name": "Rosuvastatin", "brand_names": ["Rosuvas", "Rozavel"], "strength": "10 mg", "form": "Tablet", "unit_price": 14.00, "category": "Cardiac"},
    {"generic_name": "Clopidogrel", "brand_names": ["Plavix", "Clavix"], "strength": "75 mg", "form": "Tablet", "unit_price": 10.00, "category": "Cardiac"},
    {"generic_name": "Aspirin", "brand_names": ["Ecosprin"], "strength": "75 mg", "form": "Tablet", "unit_price": 0.50, "category": "Cardiac"},

    # --- Respiratory / Cough / Cold / Allergy ---
    {"generic_name": "Cetirizine", "brand_names": ["Cetzine", "Okacet"], "strength": "10 mg", "form": "Tablet", "unit_price": 3.00, "category": "Antiallergic"},
    {"generic_name": "Levocetirizine", "brand_names": ["Levozet", "Teczine"], "strength": "5 mg", "form": "Tablet", "unit_price": 5.00, "category": "Antiallergic"},
    {"generic_name": "Montelukast + Levocetirizine", "brand_names": ["Montair-LC", "Montek-LC"], "strength": "10mg/5mg", "form": "Tablet", "unit_price": 18.00, "category": "Respiratory"},
    {"generic_name": "Salbutamol", "brand_names": ["Asthalin"], "strength": "100 mcg", "form": "Inhaler", "unit_price": 150.00, "category": "Respiratory"},
    {"generic_name": "Budesonide", "brand_names": ["Budecort"], "strength": "200 mg", "form": "Respules", "unit_price": 25.00, "category": "Respiratory"},
    {"generic_name": "Dextromethorphan + Chlorpheniramine", "brand_names": ["Ascoril-D", "Corex-DX"], "strength": "100 ml", "form": "Syrup", "unit_price": 110.00, "category": "Cough Syrup"},
    {"generic_name": "Ambroxol + Guaiphenesin + Terbutaline", "brand_names": ["Ascoril-LS", "Asthalin Expectorant"], "strength": "100 ml", "form": "Syrup", "unit_price": 105.00, "category": "Cough Syrup"},
    {"generic_name": "Povidone-iodine", "brand_names": ["Betadin"], "strength": "Standard", "form": "Gargle", "unit_price": 140.00, "category": "Respiratory"},

    # --- Vitamins / Supplements ---
    {"generic_name": "Vitamin C", "brand_names": ["Limcee", "Celin"], "strength": "500 mg", "form": "Tablet", "unit_price": 2.00, "category": "Supplement"},
    {"generic_name": "Calcium + Vitamin D3", "brand_names": ["Shelcal-500", "Cipcal-500"], "strength": "500 mg", "form": "Tablet", "unit_price": 6.00, "category": "Supplement"},
    {"generic_name": "Multivitamin", "brand_names": ["Becosules", "Supradyn", "Zincovit"], "strength": "Standard", "form": "Capsule", "unit_price": 4.00, "category": "Supplement"},
    {"generic_name": "Vitamin B12 (Methylcobalamin)", "brand_names": ["Nurokind", "Methycobal"], "strength": "1500 mcg", "form": "Tablet", "unit_price": 12.00, "category": "Supplement"},
    {"generic_name": "Vitamin E", "brand_names": ["Evion-400"], "strength": "400 mg", "form": "Capsule", "unit_price": 3.00, "category": "Supplement"},
    {"generic_name": "Iron + Folic Acid", "brand_names": ["Dexorange", "Orofer-XT"], "strength": "Standard", "form": "Tablet", "unit_price": 8.00, "category": "Supplement"},
    {"generic_name": "Cholecalciferol (Vit D3)", "brand_names": ["Uprise-D3", "Shelcal-XT"], "strength": "60K IU", "form": "Capsule", "unit_price": 40.00, "category": "Supplement"},

    # --- Dermatology / Topical ---
    {"generic_name": "Silver Sulfadiazine", "brand_names": ["Silverex", "Silvadene"], "strength": "20g", "form": "Cream", "unit_price": 85.00, "category": "Dermatology"},
    {"generic_name": "Clotrimazole", "brand_names": ["Candid"], "strength": "1% 20g", "form": "Cream", "unit_price": 60.00, "category": "Dermatology"},
    {"generic_name": "Mupirocin", "brand_names": ["T-Bact", "Mupinase"], "strength": "5g", "form": "Ointment", "unit_price": 110.00, "category": "Dermatology"},
    {"generic_name": "Permethrin", "brand_names": ["Permite"], "strength": "5% 30g", "form": "Cream", "unit_price": 70.00, "category": "Dermatology"},
    
    # --- Others / First Aid ---
    {"generic_name": "ORS (Oral Rehydration Salts)", "brand_names": ["Electral", "Walyte"], "strength": "21g", "form": "Sachet", "unit_price": 22.00, "category": "General"},
    {"generic_name": "Loperamide", "brand_names": ["Imodium", "Lopamide"], "strength": "2 mg", "form": "Tablet", "unit_price": 3.00, "category": "Gastro"},
    {"generic_name": "Sildenafil", "brand_names": ["Viagra", "Manforce"], "strength": "50 mg", "form": "Tablet", "unit_price": 25.00, "category": "General"},
    {"generic_name": "Alprazolam", "brand_names": ["Alprax", "Restyl"], "strength": "0.25 mg", "form": "Tablet", "unit_price": 4.00, "category": "Psychiatry (Restricted)"},
    {"generic_name": "Thyroxine", "brand_names": ["Eltroxin", "Thyronorm"], "strength": "50 mcg", "form": "Tablet", "unit_price": 2.00, "category": "Thyroid"},
]
