import json


def parse_vlm_result(vlm_response: str) -> dict:
    """
    Convert structured JSON returned by the VLM
    into a Python dictionary.
    """

    if not vlm_response:
        return {
            "issues": []
        }

    try:
        result = json.loads(vlm_response)

        if "issues" not in result:
            return {
                "issues": []
            }

        return result

    except json.JSONDecodeError:
        return {
            "issues": []
        }