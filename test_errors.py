import requests
import datetime
import json

BASE_URL = "http://localhost:8000/api"

def test_error_response():
    print("Testing Error Response Format...\n")
 
    past_date = (datetime.date.today() - datetime.timedelta(days=5)).isoformat()
    data_event = {
        "event_name": "Past Event",
        "event_date": past_date,
        "photographers_required": 1
    }
    
    resp = requests.post(f"{BASE_URL}/events/", json=data_event)
    if resp.status_code != 201:
        print(f"Failed to create setup event: {resp.status_code}")
        print(resp.text)
        return
    
    event_id = resp.json()['id']
    print(f"Created setup event ID: {event_id}")

    print("\nTriggering Error (Assign to past event)...")
    resp = requests.post(f"{BASE_URL}/events/{event_id}/assign-photographers/")
    
    print(f"Response Status: {resp.status_code}")
    try:
        data = resp.json()
        print("Response Body:")
        print(json.dumps(data, indent=2))
        
        if data.get("status") == "error" and "message" in data and "code" in data:
            print("\nSUCESS: Error format matches standard.")
        else:
            print("\nFAILURE: Error format does NOT match standard.")
            
    except json.JSONDecodeError:
        print("FAILURE: Response is not JSON")
        print(resp.text)

    requests.delete(f"{BASE_URL}/events/{event_id}/")

if __name__ == "__main__":
    test_error_response()
