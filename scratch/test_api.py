import httpx
import json

BASE_URL = "http://localhost:8000"

def test_full_flow():
    with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
        # 1. Health check
        res = client.get("/health")
        print("1. Health check:", res.status_code, res.json())

        # 2. Register User
        user_payload = {
            "name": "Integration Tester",
            "email": "tester@example.com",
            "password": "securepassword123"
        }
        res = client.post("/api/v1/auth/register", json=user_payload)
        print("2. Register status:", res.status_code, "text:", res.text)

        # 3. Login
        login_payload = {
            "email": "tester@example.com",
            "password": "securepassword123"
        }
        res = client.post("/api/v1/auth/login", json=login_payload)
        print("3. Login status:", res.status_code, "text:", res.text)
        token = res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 4. Create Category
        cat_payload = {"name": "Groceries"}
        res = client.post("/api/v1/categories/", json=cat_payload, headers=headers)
        print("4. Create Category:", res.status_code, res.json())
        cat_id = res.json()["id"]

        # 5. Set Budget Limit
        budget_payload = {"category_id": cat_id, "monthly_limit": 100.00}
        res = client.post("/api/v1/budgets/", json=budget_payload, headers=headers)
        print("5. Set Budget Limit:", res.status_code, res.json())

        # 6. Create Expense
        exp_payload = {
            "amount": 145.50,
            "description": "Supermarket Shopping",
            "date": "2026-07-22",
            "category_id": cat_id
        }
        res = client.post("/api/v1/expenses/", json=exp_payload, headers=headers)
        print("6. Create Expense:", res.status_code, res.json())
        exp_id = res.json()["id"]

        # 7. Upload Bill Image to MinIO
        file_data = b"Simulated receipt image binary data"
        files = {"file": ("receipt.jpg", file_data, "image/jpeg")}
        res = client.post(f"/api/v1/expenses/{exp_id}/bill", files=files, headers=headers)
        print("7. Upload Bill Image:", res.status_code, json.dumps(res.json(), indent=2))

        # 8. Retrieve Expense with Presigned Signed URL
        res = client.get(f"/api/v1/expenses/{exp_id}", headers=headers)
        print("8. Retrieve Expense Details (Signed URL):", res.status_code, json.dumps(res.json(), indent=2))

        # 9. Monthly Summary with Budget Warning Flag
        res = client.get("/api/v1/summary/monthly?year=2026&month=7", headers=headers)
        print("9. Monthly Financial Summary:", res.status_code, json.dumps(res.json(), indent=2))

        # 10. CSV Export
        res = client.get("/api/v1/expenses/export/csv?year=2026&month=7", headers=headers)
        print("10. CSV Export Response Status:", res.status_code)
        print("--- CSV Content ---")
        print(res.text)

        # 11. Logout Token Blacklisting
        res = client.post("/api/v1/auth/logout", headers=headers)
        print("11. Logout:", res.status_code, res.json())

        # 12. Verify revoked token rejected
        res = client.get("/api/v1/auth/me", headers=headers)
        print("12. Authenticate with Revoked Token (Expect 401):", res.status_code, res.json())

if __name__ == "__main__":
    test_full_flow()
