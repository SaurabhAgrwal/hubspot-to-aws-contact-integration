from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict
from app.services.aws import AWSService
from app.services.hubspot import HubSpotService
from app.models.contact import ContactResponse, SyncResponse
import os

router = APIRouter()

@router.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Service is running"}

@router.get("/contacts/aws", response_model=List[Dict])
async def get_aws_contacts():
    """Fetch contacts from AWS API"""
    try:
        aws_service = AWSService()
        contacts = await aws_service.fetch_contacts()
        return contacts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/contacts/sync", response_model=SyncResponse)
async def sync_contacts():
    try:
        # Initialize services
        aws_service = AWSService()
        hubspot_service = HubSpotService()

        # Fetch contacts from AWS
        contacts = await aws_service.fetch_contacts()
        
        # Process each contact
        results = []
        successful = 0
        failed = 0

        for contact in contacts:
            try:
                result = await hubspot_service.create_or_update_contact(contact)
                results.append({
                    "email": contact["email"],
                    "status": "success",
                    "operation": result["operation"]
                })
                successful += 1
            except Exception as e:
                results.append({
                    "email": contact["email"],
                    "status": "failed",
                    "error": str(e)
                })
                failed += 1

        return {
            "total_processed": len(contacts),
            "successful": successful,
            "failed": failed,
            "results": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/contacts/validate/{email}")
async def validate_contact(email: str):
    """Validate if a contact exists in HubSpot"""
    try:
        hubspot_service = HubSpotService()
        contact = await hubspot_service.find_contact(email)
        return {
            "exists": contact is not None,
            "details": contact if contact else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))