# Photographer Assignment System

A Django-based API to manage events and automatically assign photographers based on availability and requirements.

## Core Features

This project implements a **Smart Assignment Algorithm**:
1.  **Validation**: prevents assigning to past events or events that already have assignments.
2.  **Availability Check**: Filters photographers who are `active` and **not** assigned to any other event on the same day.
3.  **Capacity Check**: Ensures enough photographers are available before assignment; otherwise, it returns a clear error (400 Bad Request) with details.
4.  **Concurrency Safety**: Uses database transactions (`atomic`) to ensure assignments are either fully committed or rolled back.

## Setup & Installation

### Prerequisites
- Python 3.10+
- (Optional) Docker

### Local Setup

1.  **Clone the repository** (if applicable) and navigate to the `Server` directory.

2.  **Create and activate a virtual environment**:
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate
    
    # Linux/Mac
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run Migrations**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Run the Server**:
    ```bash
    python manage.py runserver
    ```

The API will be available at `http://127.0.0.1:8000/api/`.

## Docker Setup

1.  **Build the Image**:
    ```bash
    docker build -t photographer-assignment .
    ```

2.  **Run the Container**:
    ```bash
    docker run -p 8000:8000 photographer-assignment
    ```

## API Documentation

### **Events**

| Method | Endpoint | Description | Request Body Example |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/events/` | List all events | N/A |
| `POST` | `/api/events/` | Create a new event | `{"event_name": "Gala", "event_date": "2024-12-25", "photographers_required": 2}` |
| `GET` | `/api/events/<id>/` | Get event details | N/A |
| `PUT` | `/api/events/<id>/` | Update an event | `{"event_name": "Gala V2", "event_date": "2024-12-26", "photographers_required": 3}` |
| `DELETE` | `/api/events/<id>/` | Delete an event | N/A |
| `POST` | `/api/events/<id>/assign-photographers/` | **Auto-assign photographers** | `{}` (Empty body) |
| `GET` | `/api/events/<id>/assignments/` | Get photographers assigned to the event | N/A |

**Assignment Payload (POST)**: Empty body is fine (uses URL ID).

### **Photographers**

| Method | Endpoint | Description | Request Body Example |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/photographers/` | List all photographers | N/A |
| `POST` | `/api/photographers/` | Create a new photographer | `{"name": "Jane", "email": "j@test.com", "phone": "123", "is_active": true}` |
| `GET` | `/api/photographers/<id>/` | Get photographer details | N/A |
| `PUT` | `/api/photographers/<id>/` | Update photographer details | `{"name": "Jane Doe", "email": "j@test.com", "phone": "123", "is_active": false}` |
| `DELETE` | `/api/photographers/<id>/` | Delete photographer | N/A |
| `GET` | `/api/photographers/<id>/schedule/` | Get all events assigned to this photographer | N/A |

## Testing

A standard Django test suite is included to verify the logic.
```bash
python manage.py test
```
