"""
Tamil Nadu Real Estate Knowledge Base

Contains comprehensive information about real estate processes,
regulations, and requirements specific to Tamil Nadu, India.
"""

TN_KNOWLEDGE_BASE = {
    "property_registration": {
        "process": [
            "1. Document Verification - Verify all property documents including title deed, encumbrance certificate (EC), tax receipts",
            "2. Sale Agreement - Draft and execute sale agreement on stamp paper",
            "3. Payment - Pay stamp duty and registration fees",
            "4. Sub-Registrar Office - Visit the jurisdictional Sub-Registrar office",
            "5. Biometric Verification - Both parties undergo biometric verification",
            "6. Document Submission - Submit all required documents",
            "7. Registration - Complete registration process and receive registered sale deed",
            "8. Mutation - Apply for property tax mutation with local body"
        ],
        "timeline": "Typically 1-2 weeks after document preparation",
        "authorities": ["Sub-Registrar Office", "Tamil Nadu Registration Department"]
    },
    
    "required_documents": {
        "buyer": [
            "PAN Card",
            "Aadhaar Card",
            "Address Proof",
            "Passport-size photographs",
            "Bank account details (for loan cases)"
        ],
        "seller": [
            "Original Sale Deed / Title Deed",
            "Encumbrance Certificate (EC) for last 13-30 years",
            "Property Tax Receipts (last 3 years)",
            "Approved Building Plan (for constructed properties)",
            "Completion Certificate (if applicable)",
            "NOC from Society/Apartment (if applicable)",
            "PAN Card and Aadhaar Card"
        ],
        "property": [
            "Parent Document (previous sale deed)",
            "Patta and Chitta (land ownership records)",
            "Survey Number details",
            "Layout Approval from DTCP/CMDA (for plots)",
            "Occupancy Certificate (for buildings)"
        ]
    },
    
    "authorities": {
        "TNRERA": {
            "name": "Tamil Nadu Real Estate Regulatory Authority",
            "role": "Regulates real estate projects and protects buyer interests",
            "website": "https://rera.tn.gov.in",
            "mandate": "All projects above 500 sq.m or 8 apartments must be registered"
        },
        "DTCP": {
            "name": "Directorate of Town and Country Planning",
            "role": "Approves layout plans and ensures planned development",
            "jurisdiction": "Areas outside Chennai Corporation limits"
        },
        "CMDA": {
            "name": "Chennai Metropolitan Development Authority",
            "role": "Planning authority for Chennai Metropolitan Area",
            "jurisdiction": "Chennai and surrounding areas"
        },
        "Sub_Registrar": {
            "name": "Sub-Registrar Office",
            "role": "Property registration and document verification",
            "location": "Based on property location jurisdiction"
        }
    },
    
    "stamp_duty_registration": {
        "stamp_duty": "7% of property value (for properties above ₹50 lakhs in urban areas)",
        "registration_fee": "1% of property value (maximum ₹1 lakh)",
        "women_benefit": "2% discount on stamp duty for properties registered in women's names",
        "calculation": "Based on guideline value or transaction value, whichever is higher"
    },
    
    "measurement_units": {
        "cent": {
            "definition": "A cent is a common land measurement unit in South India, especially Tamil Nadu",
            "conversion": "1 cent = 435.6 square feet = 40.47 square meters",
            "usage": "Commonly used for residential plots and small land parcels",
            "example": "A standard residential plot might be 3-5 cents (1,300-2,200 sq ft)"
        },
        "ground": {
            "definition": "Ground is another traditional measurement unit used in Tamil Nadu",
            "conversion": "1 ground = 2,400 square feet = 222.97 square meters",
            "relation": "1 ground = approximately 5.5 cents"
        },
        "acre": {
            "definition": "Acre is used for larger land parcels",
            "conversion": "1 acre = 43,560 square feet = 4,047 square meters = 100 cents",
            "usage": "Used for agricultural land and large plots"
        },
        "gunta": {
            "definition": "Gunta (also called guntha) is used in some parts of Tamil Nadu",
            "conversion": "1 gunta = 1,089 square feet = 101.17 square meters",
            "relation": "40 guntas = 1 acre"
        },
        "common_conversions": [
            "1 cent = 435.6 sq ft",
            "1 ground = 2,400 sq ft = 5.5 cents",
            "1 acre = 100 cents = 43,560 sq ft",
            "1 gunta = 1,089 sq ft = 2.5 cents"
        ]
    },
    
    "red_flags": [
        "Property without clear title or disputed ownership",
        "Encumbrance Certificate showing pending loans or legal cases",
        "Unapproved layouts by DTCP/CMDA",
        "Properties in prohibited areas (poramboke land, water bodies)",
        "Missing or fake completion certificates",
        "Developer not registered with TNRERA (for new projects)",
        "Significant difference between guideline value and asking price",
        "Seller unwilling to provide complete documentation",
        "Properties with pending property tax dues",
        "Land use conversion not approved (agricultural to residential)"
    ],
    
    "bank_loan": {
        "eligibility": [
            "Age: 21-65 years (varies by bank)",
            "Income: Stable monthly income (salaried/self-employed)",
            "Credit Score: Minimum 750 recommended",
            "Employment: Minimum 2-3 years work experience"
        ],
        "documents": [
            "Loan application form",
            "Identity and address proof",
            "Income proof (salary slips, ITR, bank statements)",
            "Property documents for verification",
            "Processing fee payment proof"
        ],
        "process": [
            "1. Loan application and eligibility check",
            "2. Property document verification by bank",
            "3. Property valuation by bank-approved valuers",
            "4. Legal verification of title",
            "5. Loan sanction letter",
            "6. Disbursement after registration"
        ],
        "loan_to_value": "Usually 75-90% of property value",
        "tenure": "Up to 30 years"
    },
    
    "chennai_specific": {
        "zones": ["North Chennai", "Central Chennai", "South Chennai", "West Chennai"],
        "planning_authority": "CMDA (Chennai Metropolitan Development Authority)",
        "property_tax": "Collected by Greater Chennai Corporation",
        "water_connection": "Chennai Metro Water (CMWSSB)",
        "electricity": "Tangedco (Tamil Nadu Generation and Distribution Corporation)"
    }
}


def get_knowledge_context(query_lower: str) -> str:
    """
    Get relevant knowledge base context based on query keywords.
    
    Args:
        query_lower: Lowercase user query
        
    Returns:
        Relevant context string
    """
    context_parts = []
    
    # Check for registration-related queries
    if any(word in query_lower for word in ['register', 'registration', 'sub-registrar', 'பதிவு']):
        context_parts.append("PROPERTY REGISTRATION PROCESS:\n" + 
                           "\n".join(TN_KNOWLEDGE_BASE['property_registration']['process']))
    
    # Check for document-related queries
    if any(word in query_lower for word in ['document', 'documents', 'papers', 'ஆவணம்', 'ஆவணங்கள்']):
        docs = TN_KNOWLEDGE_BASE['required_documents']
        context_parts.append(f"REQUIRED DOCUMENTS:\nBuyer: {', '.join(docs['buyer'])}\n" +
                           f"Seller: {', '.join(docs['seller'][:5])}\n" +
                           f"Property: {', '.join(docs['property'][:4])}")
    
    # Check for loan-related queries
    if any(word in query_lower for word in ['loan', 'bank', 'finance', 'கடன்', 'வங்கி']):
        loan = TN_KNOWLEDGE_BASE['bank_loan']
        context_parts.append(f"BANK LOAN INFORMATION:\nEligibility: {', '.join(loan['eligibility'][:3])}\n" +
                           f"Process: {', '.join(loan['process'][:4])}")
    
    # Check for stamp duty queries
    if any(word in query_lower for word in ['stamp', 'duty', 'fee', 'charges', 'முத்திரை']):
        stamp = TN_KNOWLEDGE_BASE['stamp_duty_registration']
        context_parts.append(f"STAMP DUTY & REGISTRATION:\n" +
                           f"Stamp Duty: {stamp['stamp_duty']}\n" +
                           f"Registration Fee: {stamp['registration_fee']}\n" +
                           f"Women Benefit: {stamp['women_benefit']}")
    
    # Check for measurement unit queries
    if any(word in query_lower for word in ['cent', 'cents', 'ground', 'acre', 'gunta', 'sqft', 'square feet', 'measurement', 'size', 'area']):
        units = TN_KNOWLEDGE_BASE['measurement_units']
        context_parts.append(f"LAND MEASUREMENT UNITS IN TAMIL NADU:\n" +
                           f"Cent: {units['cent']['conversion']} - {units['cent']['usage']}\n" +
                           f"Ground: {units['ground']['conversion']} - {units['ground']['relation']}\n" +
                           f"Acre: {units['acre']['conversion']}\n" +
                           f"Common conversions: {', '.join(units['common_conversions'][:3])}")
    
    # Check for authority-related queries
    if any(word in query_lower for word in ['tnrera', 'rera', 'dtcp', 'cmda', 'authority']):
        context_parts.append("KEY AUTHORITIES:\n" +
                           "TNRERA: Regulates real estate projects\n" +
                           "DTCP: Approves layouts outside Chennai\n" +
                           "CMDA: Planning authority for Chennai")
    
    return "\n\n".join(context_parts) if context_parts else ""
