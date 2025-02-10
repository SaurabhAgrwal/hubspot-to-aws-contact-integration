import httpx
from typing import List, Dict

class AWSService:
    def __init__(self):
        self.api_url = "https://l0hefgbbla.execute-api.us-east-1.amazonaws.com/prod/contacts"
        self.bearer_token = "76420678-F678-4D22-A29D-0D4A26313D26"
        self.fetched_ids = set()
        self.offset = 0
        self.batch_size = 20

    async def fetch_contacts(self) -> List[Dict]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.api_url,
                headers={"Authorization": f"Bearer {self.bearer_token}"}
            )
            response.raise_for_status()
            contacts = response.json()

            new_contacts = []
            duplicates = []

            for contact in contacts[self.offset : self.offset + self.batch_size]:
                contact_id = contact.get("id")
                if contact_id in self.fetched_ids:
                    duplicates.append(contact)
                else:
                    new_contacts.append(contact)
                    self.fetched_ids.add(contact_id)

            self.offset += self.batch_size

            if duplicates:
                print("Duplicate Contacts Found:", duplicates)

            return new_contacts