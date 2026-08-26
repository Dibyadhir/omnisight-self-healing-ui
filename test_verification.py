from backend.services.verification import parse_verification_result


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


if __name__ == "__main__":
    test_verified_result()
    test_unverified_result()
    test_markdown_json_result()

    print("\nAll verification tests passed.")