  export interface EmailResponse {
    sender: string;
    subject: string;
    request_type?: string; // Optional because it might be null
    sub_request_type?: string; // Optional because it might be null
    confidence_score?: number; // Optional because it might be null
    duplicate_flag: boolean;
    all_extracted_numbers: any;
    // ... other properties from your EmailData model
  }
  