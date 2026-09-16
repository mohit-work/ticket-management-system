def test_get_ticket(client):
    response = client.get("/tickets/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == "Laptop cannot connect to office Wi-Fi"


def test_get_missing_ticket(client):
    response = client.get("/tickets/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket not found"


def test_invalid_ticket_status(client):
    response = client.put(
        "/tickets/1",
        json={"status": "INVALID"}
    )

    assert response.status_code == 422


def test_invalid_ticket_transition(client):
    response = client.put(
        "/tickets/1",
        json={"status": "OPEN"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot change status from CLOSED to OPEN"


def test_create_ticket(client):
    response = client.post(
        "/tickets/",
        json={
            "employee_id": 1,
            "engineer_id": 1,
            "title": "VPN connection issue",
            "description": "Unable to connect to company VPN.",
            "category": "Network",
            "priority": "MEDIUM"
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "VPN connection issue"
    assert response.json()["status"] == "OPEN"


def test_filter_tickets_by_status(client):
    response = client.get("/tickets/?status=OPEN")

    assert response.status_code == 200

    for ticket in response.json():
        assert ticket["status"] == "OPEN"


def test_filter_tickets_by_priority(client):
    response = client.get("/tickets/?priority=HIGH")

    assert response.status_code == 200

    for ticket in response.json():
        assert ticket["priority"] == "HIGH"


def test_filter_tickets_by_category(client):
    response = client.get("/tickets/?category=Network")

    assert response.status_code == 200

    for ticket in response.json():
        assert ticket["category"] == "Network"


def test_filter_tickets_combined(client):
    response = client.get(
        "/tickets/?status=OPEN&priority=MEDIUM"
    )

    assert response.status_code == 200

    for ticket in response.json():
        assert ticket["status"] == "OPEN"
        assert ticket["priority"] == "MEDIUM"


def test_get_ticket_updates(client):
    response = client.get("/tickets/1/updates")

    assert response.status_code == 200

    updates = response.json()

    assert len(updates) >= 1

    for update in updates:
        assert update["ticket_id"] == 1
        assert update["engineer_id"] == 1
        assert update["new_status"] is not None


def test_get_updates_missing_ticket(client):
    response = client.get("/tickets/999/updates")

    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket not found"


def test_get_employees(client):
    response = client.get("/employees/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_employee(client):
    response = client.get("/employees/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_create_employee(client):
    response = client.post(
        "/employees/",
        json={
            "name": "Test Employee",
            "email": "test.employee@example.com",
            "department": "IT"
        }
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Test Employee"
    assert response.json()["department"] == "IT"


def test_get_engineers(client):
    response = client.get("/engineers/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_engineer(client):
    response = client.get("/engineers/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_create_engineer(client):
    response = client.post(
        "/engineers/",
        json={
            "name": "Test Engineer",
            "email": "test.engineer@example.com",
            "specialization": "Network"
        }
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Test Engineer"
    assert response.json()["specialization"] == "Network"

def test_create_ticket_with_missing_employee(client):
    response = client.post(
        "/tickets/",
        json={
            "employee_id": 9999,
            "engineer_id": 1,
            "title": "Wi-Fi issue",
            "description": "Laptop cannot connect to office Wi-Fi",
            "category": "Network",
            "priority": "HIGH"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Employee not found"


def test_create_ticket_with_missing_engineer(client):
    response = client.post(
        "/tickets/",
        json={
            "employee_id": 1,
            "engineer_id": 9999,
            "title": "Wi-Fi issue",
            "description": "Laptop cannot connect to office Wi-Fi",
            "category": "Network",
            "priority": "HIGH"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Engineer not found"

def test_update_ticket_with_missing_engineer(client):
    response = client.put(
        "/tickets/1",
        json={
            "engineer_id": 9999
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Engineer not found"

def test_create_employee_with_duplicate_email(client):
    response = client.post(
        "/employees/",
        json={
            "name": "Duplicate Employee",
            "email": "seed.employee@example.com",
            "department": "IT"
        }
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Email already exists"


def test_create_engineer_with_duplicate_email(client):
    response = client.post(
        "/engineers/",
        json={
            "name": "Duplicate Engineer",
            "email": "seed.engineer@example.com",
            "specialization": "Network"
        }
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Email already exists"

def test_update_ticket_details(client):
    response = client.put(
        "/tickets/1",
        json={
            "engineer_id": 1,
            "title": "Updated Wi-Fi Issue",
            "description": "Updated description",
            "category": "Software",
            "priority": "MEDIUM"
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert data["engineer_id"] == 1
    assert data["title"] == "Updated Wi-Fi Issue"
    assert data["description"] == "Updated description"
    assert data["category"] == "Software"
    assert data["priority"] == "MEDIUM"