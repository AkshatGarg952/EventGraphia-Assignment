
import requests
import datetime
import sys

BASE_URL = "http://127.0.0.1:8000/api"

def run_test():
    with open("test_output.txt", "w") as f:
       
        create_payload = {
            "event_name": "Test Event",
            "event_date": str(datetime.date.today() + datetime.timedelta(days=10)),
            "photographers_required": 2
        }
        
        f.write(f"Creating event with payload: {create_payload}\n")
        response = requests.post(f"{BASE_URL}/events/", json=create_payload)
        if response.status_code != 201:
            f.write(f"Failed to create event. Status: {response.status_code}\n")
            f.write(response.text + "\n")
            return

        event_id = response.json()['id']
        f.write(f"Event created with ID: {event_id}\n")

        patch_payload = {
            "event_name": "Updated Event Name (PATCH)"
        }
        f.write(f"\nTesting PATCH with payload: {patch_payload}\n")
        response = requests.patch(f"{BASE_URL}/events/{event_id}/", json=patch_payload)
        
        if response.status_code == 200:
            f.write("PATCH successful!\n")
            f.write(f"Updated Event: {response.json()}\n")
        else:
            f.write(f"PATCH failed. Status: {response.status_code}\n")
            f.write(response.text + "\n")

        put_payload = {
            "event_name": "Updated Event Name (PUT)"
        }
        f.write(f"\nTesting PUT with partial payload (Expected to fail): {put_payload}\n")
        response = requests.put(f"{BASE_URL}/events/{event_id}/", json=put_payload)
        
        if response.status_code == 200:
            f.write("PUT successful (Unexpected for partial data)!\n")
            f.write(f"Updated Event: {response.json()}\n")
        else:
            f.write(f"PUT failed as expected for partial data. Status: {response.status_code}\n")
            f.write(response.text + "\n")

if __name__ == "__main__":
    try:
        run_test()
    except Exception as e:
        print(f"An error occurred: {e}")
