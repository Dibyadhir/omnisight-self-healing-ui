from fastapi.testclient import TestClient
from backend.main import app
from backend.services.verification import parse_verification_result


client = TestClient(app)


def test_verified_result():
    response = """
    {
        "verified": true,
        "analysis": "The checkout button is now properly aligned."
    }
    """

    result = parse_verification_result(response)

    assert result["verified"] is True
    assert "properly aligned" in result["analysis"]

    print("PASS: Verified UI result")


def test_unverified_result():
    response = """
    {
        "verified": false,
        "analysis": "The checkout button is still misaligned."
    }
    """

    result = parse_verification_result(response)

    assert result["verified"] is False
    assert "still misaligned" in result["analysis"]

    print("PASS: Unverified UI result")


def test_markdown_json_result():
    response = """
    ```json
    {
        "verified": true,
        "analysis": "The UI issue has been fixed."
    }
    ```
    """

    result = parse_verification_result(response)

    assert result["verified"] is True
    assert "issue has been fixed" in result["analysis"]

    print("PASS: Markdown JSON result")


def test_empty_input_validation():
    response = client.post(
        "/api/analyze",
        json={
            "screenshot": "",
            "dom": ""
        }
    )

    assert response.status_code == 422
    assert "At least screenshot or DOM must be provided" in response.text

    print("PASS: Empty input validation")


def test_invalid_screenshot_type():
    response = client.post(
        "/api/analyze",
        json={
            "screenshot": 12345,
            "dom": "<button>Checkout</button>"
        }
    )

    assert response.status_code == 422

    print("PASS: Invalid screenshot type validation")


def test_dom_only_validation():
    response = client.post(
        "/api/analyze",
        json={
            "screenshot": "",
            "dom": "<button>Checkout</button>"
        }
    )

    # Request validation should pass.
    # The endpoint may call the VLM service afterwards.
    assert response.status_code != 422

    print("PASS: DOM-only input validation")


if __name__ == "__main__":
    test_verified_result()
    test_unverified_result()
    test_markdown_json_result()

    test_empty_input_validation()
    test_invalid_screenshot_type()
    test_dom_only_validation()

    print("\nAll verification and API validation tests passed.")