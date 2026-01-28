import pytest
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
@patch("app.clients.hospital_client.HospitalClient.create_hospital", new_callable=AsyncMock)
@patch("app.clients.hospital_client.HospitalClient.activate_batch", new_callable=AsyncMock)
async def test_bulk_upload_success(mock_activate, mock_create, client):
    mock_create.return_value = {"id": 1}
    mock_activate.return_value = {}

    csv_content = "name,address,phone\nA Hospital,NY,1234567"

    response = await client.post(
        "/hospitals/bulk",
        files={"file": ("test.csv", csv_content, "text/csv")},
    )

    data = response.json()

    assert response.status_code == 201
    assert data["success"] is True
    assert data["data"]["processed"] == 1
    assert data["data"]["failed"] == 0
    mock_activate.assert_called_once()


@pytest.mark.asyncio
async def test_get_status_not_found(client):
    response = await client.get("/hospitals/bulk/invalid-id")

    assert response.status_code == 404
    assert response.json()["success"] is False


@pytest.mark.asyncio
async def test_validate_endpoint_success(client):
    csv_content = "name,address,phone\nA Hospital,NY,1234567"

    response = await client.post(
        "/hospitals/bulk/validate",
        files={"file": ("test.csv", csv_content, "text/csv")},
    )

    data = response.json()
    assert response.status_code == 200
    assert data["success"] is True
    assert data["data"]["valid"] is True
