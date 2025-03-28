# Patient Service - Entity Relationship Diagram

This diagram illustrates the database schema for the Patient Service.

```mermaid
erDiagram
    PATIENT {
        uuid id PK
        string first_name
        string last_name
        date date_of_birth
        string gender
        string email
        string phone
        string address
        string insurance_provider
        string insurance_number
        uuid user_id FK
        timestamps created_updated
    }
    
    MEDICAL_RECORD {
        uuid id PK
        uuid patient_id FK
        string record_type
        text description
        date record_date
        uuid practitioner_id
        timestamps created_updated
    }
    
    ATTACHMENT {
        uuid id PK
        uuid patient_id FK
        uuid medical_record_id FK
        string file_name
        string file_type
        string file_url
        timestamps created_updated
    }
    
    PATIENT_PRACTITIONER {
        uuid patient_id FK
        uuid practitioner_id FK
        date assigned_date
        string access_level
        boolean is_primary
        timestamps created_updated
    }
    
    PATIENT ||--o{ MEDICAL_RECORD : "has"
    PATIENT ||--o{ ATTACHMENT : "has"
    MEDICAL_RECORD ||--o{ ATTACHMENT : "has"
    PATIENT ||--o{ PATIENT_PRACTITIONER : "assigned to"
```

## Schema Description

### PATIENT
Stores core patient information including personal details, contact information, and insurance data.

### MEDICAL_RECORD
Contains medical history records for patients, linked to the patient who owns the record.

### ATTACHMENT
Manages file attachments such as medical documents, X-rays, or referral letters.

### PATIENT_PRACTITIONER
Junction table that manages the relationships between patients and practitioners.
