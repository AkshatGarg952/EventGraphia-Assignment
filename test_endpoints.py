import requests
import json
import datetime

BASE_URL = "http://localhost:8000/api"

def print_result(step, response, expected_status=None):
    if expected_status and response.status_code != expected_status:
        print(f"{step} Failed: Expected {expected_status}, got {response.status_code}")
        print(f"Response: {response.text}")
    else:
        print(f"{step} Passed ({response.status_code})")
        if response.text and len(response.text) < 200:
           print(f"   Output: {response.text}")

def test_api():
    print("Starting API Tests...\n")
    
    print("--- 1. Photographer Management ---")
    data_photographer = {
        "name": "Test Photographer",
        "email": f"test_{datetime.datetime.now().timestamp()}@example.com",
        "phone": "555-0199",
        "is_active": True
    }
    resp = requests.post(f"{BASE_URL}/photographers/", json=data_photographer)
    print_result("Create Photographer", resp, 201)
    if resp.status_code != 201:
        return
    photographer_id = resp.json()['id']

    resp = requests.get(f"{BASE_URL}/photographers/")
    print_result("List Photographers", resp, 200)

    resp = requests.get(f"{BASE_URL}/photographers/{photographer_id}/")
    print_result("Get Photographer Details", resp, 200)

    update_data = {"phone": "555-9999"}
    resp = requests.put(f"{BASE_URL}/photographers/{photographer_id}/", json={**data_photographer, **update_data})
    print_result("Update Photographer", resp, 200)

    print("\n--- 2. Event Management ---")
    data_event = {
        "event_name": "Test Gala",
        "event_date": (datetime.date.today() + datetime.timedelta(days=30)).isoformat(),
        "photographers_required": 1
    }
    resp = requests.post(f"{BASE_URL}/events/", json=data_event)
    print_result("Create Event", resp, 201)
    if resp.status_code != 201:
        return
    event_id = resp.json()['id']

    resp = requests.get(f"{BASE_URL}/events/")
    print_result("List Events", resp, 200)

    resp = requests.get(f"{BASE_URL}/events/{event_id}/")
    print_result("Get Event Details", resp, 200)

    resp = requests.patch(f"{BASE_URL}/events/{event_id}/", json={"photographers_required": 2})
    print_result("Update Event", resp, 200)

    print("\n--- 3. Assignments ---")
    resp = requests.post(f"{BASE_URL}/events/{event_id}/assign-photographers/")
    print_result("Assign Photographers (Algorithm)", resp, 200)

    resp = requests.get(f"{BASE_URL}/events/{event_id}/assignments/")
    print_result("Get Event Assignments", resp, 200)

    resp = requests.get(f"{BASE_URL}/photographers/{photographer_id}/schedule/")
    print_result("Get Photographer Schedule", resp, 200)


    print("\n--- 4. Data Cleanup (Optional) ---")
    resp = requests.delete(f"{BASE_URL}/events/{event_id}/")
    print_result("Delete Event", resp, 204)

    resp = requests.delete(f"{BASE_URL}/photographers/{photographer_id}/")
    print_result("Delete Photographer", resp, 204)

    print("\n All tests completed.")

if __name__ == "__main__":
    try:
        try:
             requests.get(BASE_URL.replace("/api", "/admin/login/"), timeout=2)
        except requests.exceptions.ConnectionError:
            print(f"Could not connect to {BASE_URL}")
            print(" Running the server is required. Please run: 'python manage.py runserver'")
            exit(1)
            
        test_api()
    except ImportError:
        print(" 'requests' library not found. Run: pip install requests")
