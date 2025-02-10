import httpx
import os
from typing import Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class HubSpotService:
    
    def __init__(self):
        self.api_key = os.getenv("HUBSPOT_API_KEY")
        if not self.api_key:
            raise ValueError("HUBSPOT_API_KEY environment variable is required")
        
        self.base_url = "https://api.hubapi.com"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def find_contact(self, email: str) -> Optional[Dict]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/contacts/v1/contact/email/{email}/profile",
                headers=self.headers
            )
            return response.json() if response.status_code == 200 else None

    async def create_or_update_contact(self, contact_data: Dict) -> Dict:
        
        properties = {
            "email": contact_data["email"],
            "firstname": contact_data["first_name"],
            "lastname": contact_data["last_name"],
            "phone": contact_data.get("phone_number", ""),
            "company": contact_data.get("company", "")
        }

        # Debugging: Print the properties that are being sent to HubSpot
        print("Mapped Properties:", properties)

        # Check if contact exists
        existing_contact = await self.find_contact(properties["email"])

        async with httpx.AsyncClient() as client:
            if existing_contact:
                # Update existing contact
                print(f"Updating contact with email {properties['email']}")
                response = await client.patch(
                    f"{self.base_url}/crm/v3/objects/contacts/{existing_contact['vid']}",
                    headers=self.headers,
                    json={"properties": properties}
                )
                response.raise_for_status()
                return {"operation": "updated", "data": response.json()}
            else:
                response = await client.post(
                    f"{self.base_url}/crm/v3/objects/contacts",
                    headers=self.headers,
                    json={"properties": properties}
                )
                response.raise_for_status()
                return {"operation": "created", "data": response.json()}
