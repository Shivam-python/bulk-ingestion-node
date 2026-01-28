import pytest
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
@patch("app.clients.hospital_client.HospitalClient.create_hospital", new_callable=AsyncMock)
async def test_partial_failure_no_activation(mock_create, client):
    # First hospital succeeds, second fails
    mock_create.side_effect = [{"id": 1}, Exception("API down")]

    csv_content = "name,address,phone\nA Hospital,NY,123\nB Hospital,CA,456"

    response = await client.post(
        "/hospitals/bulk",
        files={"file": ("test.csv", csv_content, "text/csv")},
    )

    data = response.json()
    assert data["data"]["failed"] == 1
    assert data["data"]["activated"] is False


@pytest.mark.asyncio
async def test_invalid_csv_upload(client):
    csv_content = "wrong,data"

    response = await client.post(
        "/hospitals/bulk",
        files={"file": ("bad.csv", csv_content, "text/csv")},
    )

    assert response.status_code == 422
    assert response.json()["success"] is False
