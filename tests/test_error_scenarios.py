import pytest
from unittest.mock import AsyncMock, patch


import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from app.core.state import BATCH_STORE


@pytest.mark.asyncio
@patch("app.clients.hospital_client.HospitalClient.activate_batch", new_callable=AsyncMock)
@patch("app.clients.hospital_client.HospitalClient.create_hospital", new_callable=AsyncMock)
async def test_partial_failure_no_activation(mock_create, mock_activate, client):

    # First succeeds, second fails
    mock_create.side_effect = [{"id": 1}, Exception("API down")]

    csv_content = "name,address,phone\nA Hospital,NY,123\nB Hospital,CA,456"

    # Start bulk job
    response = await client.post(
        "/hospitals/bulk",
        files={"file": ("test.csv", csv_content, "text/csv")},
    )

    assert response.status_code == 202
    batch_id = response.json()["data"]["batch_id"]

    # Wait for background task to finish
    await asyncio.sleep(0.2)

    batch = BATCH_STORE[batch_id]

    assert batch["processed"] == 1
    assert batch["failed"] == 1
    assert batch["activated"] is False
    mock_activate.assert_not_called()



@pytest.mark.asyncio
async def test_invalid_csv_upload(client):
    csv_content = "wrong,data"

    response = await client.post(
        "/hospitals/bulk/validate",
        files={"file": ("bad.csv", csv_content, "text/csv")},
    )

    assert response.status_code == 422
    assert response.json()["success"] is False
