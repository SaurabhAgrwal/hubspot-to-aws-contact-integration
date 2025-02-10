# AWS to HubSpot Contact Integration

A professional API service that syncs contacts from AWS to HubSpot, with proper error handling and duplicate management.

## Features

- ✨ AWS Contact Data Fetching
- 🔄 HubSpot Contact Sync
- 📝 Duplicate Contact Management
- 🚀 FastAPI-based REST API
- 📊 Detailed Sync Reports

## Setup Instructions

### 1. Clone the repository:
```bash
git clone [<repository-url>](https://github.com/SaurabhAgrwal/hubspot-to-aws-contact-integration)
cd hubspot_integration
```

### 2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

### 4. Configure environment:
```bash
cp .env.example .env  # Rename the environment file
# Edit .env and add your HubSpot API key and AWS credentials
```

## Running the Application

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Health Check
#### Check if the API is running:
```http
GET /api/v1/health
```
**Response:**
```json
{
  "status": "healthy",
  "message": "Service is running"
}
```

---

### 2. List AWS Contacts
#### Fetch contacts from AWS:
```http
GET /api/v1/contacts/aws
```
**Response:**
```json
[
  {
    "id": 1,
    "first_name": "Phillipp",
    "last_name": "Cavil",
    "email": "pcavil0@posterous.com",
    "gender": "Male",
    "phone_number": "(368) 9290182"
  },
  {
    "id": 2,
    "first_name": "Obidiah",
    "last_name": "Mc Gee",
    "email": "omcgee1@a8.net",
    "gender": "Male",
    "phone_number": "(441) 6670412"
  }
]
```

---

### 3. Sync Contacts
#### Sync AWS contacts to HubSpot:
```http
POST /api/v1/contacts/sync
```
**Response:**
```json
{
  "total_processed": 3,
  "successful": 3,
  "failed": 0,
  "results": [
    {
      "email": "pcavil0@posterous.com",
      "status": "success",
      "operation": "updated"
    },
    {
      "email": "omcgee1@a8.net",
      "status": "success",
      "operation": "updated"
    },
    {
      "email": "nsmallthwaite2@ebay.com",
      "status": "success",
      "operation": "updated"
    }
  ]
}
```

---

### 4. Validate Contact
#### Check if a contact exists in HubSpot:
```http
GET /api/v1/contacts/validate/{email}
```
**Example:**
```http
GET /api/v1/contacts/validate/awightj@hud.gov
```
**Response:**
```json
{
  "exists": true,
  "details": {
    "vid": 98298151813,
    "canonical-vid": 98298151813,
    "merged-vids": [],
    "portal-id": 48907631,
    "is-contact": true,
    "properties": {
      "num_unique_conversion_events": {
        "value": "0",
        "versions": [
          {
            "value": "0",
            "source-type": "CALCULATED",
            "timestamp": 1739181961824
          }
        ]
      }
    }
  }
}
```

## API Documentation

Once the application is running, access:
- **Swagger UI:** `http://localhost:8000/docs`

## Security Measures

- API keys are managed through environment variables
- No sensitive information is committed to the repository
- CORS middleware configured for security

## Error Handling

- Comprehensive error handling for API calls
- Detailed error messages in responses
- Proper HTTP status codes for all API responses


