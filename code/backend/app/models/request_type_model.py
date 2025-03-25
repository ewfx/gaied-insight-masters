class RequestTypeModel:
    requests_datasets = [
    {
        "Request Type": "Adjustment",
        "Sub-Request Type": ["N/A"],
    },
    {
        "Request Type": "AU Transfer",
        "Sub-Request Type": ["N/A"],
    },
    {
        "Request Type": "Closing Notice",
        "Sub-Request Type": ["Reallocation Fees", "Amendment Fees", "Reallocation Principal"],
    },
    {
        "Request Type": "Commitment Change",
        "Sub-Request Type": ["Cashless Roll", "Decrease", "Increase"],
    },
    {
        "Request Type": "Fee Payment",
        "Sub-Request Type": ["Ongoing Fee", "Letter of Credit Fee"],
    },
    {
        "Request Type": "Money Movement - Inbound",
        "Sub-Request Type": ["Principal", "Interest", "Principal + Interest", "Principal + Interest + Fee"],
    },
    {
        "Request Type": "Money Movement - Outbound",
        "Sub-Request Type": ["Timebound", "Foreign Currency"],
    },
    {
        "Request Type": "Account Opening",
        "Sub-Request Type": ["Checking Account", "Savings Account", "Money Market Account", "Certificate of Deposit (CD)"],
    },
    {
        "Request Type": "Account Closing",
        "Sub-Request Type": ["Checking Account", "Savings Account", "Money Market Account", "Certificate of Deposit (CD)"],
    },
    {
        "Request Type": "Balance Inquiry",
        "Sub-Request Type": ["Checking Account", "Savings Account", "Loan Account", "Credit Card Account"],
    },
    {
        "Request Type": "Statement Request",
        "Sub-Request Type": ["Checking Account", "Savings Account", "Loan Account", "Credit Card Account"],
    },
    {
        "Request Type": "Transaction History Request",
        "Sub-Request Type": ["Checking Account", "Savings Account", "Loan Account", "Credit Card Account"],
    },
    {
        "Request Type": "Funds Transfer",
        "Sub-Request Type": ["Internal Transfer", "External Transfer (ACH, Wire)"],
    },
    {
        "Request Type": "Stop Payment",
        "Sub-Request Type": ["Check", "Electronic Transfer"],
    },
    {
        "Request Type": "Credit Card Application",
        "Sub-Request Type": ["Personal", "Business"],
    },
    {
        "Request Type": "Credit Limit Change",
        "Sub-Request Type": ["Increase", "Decrease"],
    },
    {
        "Request Type": "Loan Application",
        "Sub-Request Type": ["Mortgage", "Auto Loan", "Personal Loan", "Business Loan"],
    },
    {
        "Request Type": "Loan Disbursement",
        "Sub-Request Type": ["Initial Disbursement", "Subsequent Disbursement"],
    },
    {
        "Request Type": "Loan Payoff",
        "Sub-Request Type": ["Principal", "Interest", "Fees"],
    },
    {
        "Request Type": "Customer Information Update",
        "Sub-Request Type": ["Address Change", "Phone Number Change", "Email Address Change"],
    },
    {
        "Request Type": "Online/Mobile Banking Access",
        "Sub-Request Type": ["Enrollment", "Password Reset", "Access Removal"],
    },
    {
        "Request Type": "Security Request",
        "Sub-Request Type": ["Change PIN", "Report Lost/Stolen Card", "Fraud Alert"],
    }
]
    
    @classmethod
    def get_sub_types(cls, request_type):
        """Retrieve sub-request types based on the request type"""
        for item in cls.requests_datasets:
            if item["Request Type"] == request_type:
                return item["Sub-Request Type"]
        return []
