from app.utils.csv_validator import validate_csv, CSVValidationError


def test_valid_csv():
    content = "name,address,phone\nA Hospital,NY,1234567"
    result = validate_csv(content)
    assert result["valid"] is True
    assert result["total_rows"] == 1


def test_missing_required_header():
    content = "name,phone\nHospital A,123"
    try:
        validate_csv(content)
    except CSVValidationError as e:
        assert "Missing required headers" in str(e)


def test_exceed_row_limit():
    rows = "\n".join([f"Hospital{i},Addr{i},1234567" for i in range(21)])
    content = "name,address,phone\n" + rows

    try:
        validate_csv(content)
    except CSVValidationError as e:
        assert "Maximum 20 hospitals" in str(e)


def test_duplicate_hospital_detection():
    content = "name,address,phone\nA,Addr,123\nA,Addr,456"
    result = validate_csv(content)
    assert result["valid"] is False
    assert "Duplicate hospital entry" in result["errors"][0]
