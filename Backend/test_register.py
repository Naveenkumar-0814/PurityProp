import httpx
import asyncio

async def test_register():
    url = "http://127.0.0.1:8000/api/auth/register"
    payload = {
        "email": "test2@example.com",
        "password": "Password123!",
        "name": "Test User"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            print(f"Sending POST to {url} with {payload}...")
            response = await client.post(url, json=payload, timeout=10.0)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_register())
