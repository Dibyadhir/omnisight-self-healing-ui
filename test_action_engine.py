from pathlib import Path

from backend.services.action_engine import apply_css_fix


TEST_CSS = Path("test_style.css")


# Create temporary CSS file
TEST_CSS.write_text(
    """
body {
    margin: 0;
}
""",
    encoding="utf-8"
)


valid_css = """
@media (max-width: 768px) {
    .navbar-nav {
        flex-direction: column;
    }
}
"""


invalid_css = """
<div>
    This is HTML
</div>
"""


print("VALID CSS TEST")
result = apply_css_fix(
    str(TEST_CSS),
    valid_css,
    backup=True
)

print(result)


print("\nINVALID CSS TEST")
result = apply_css_fix(
    str(TEST_CSS),
    invalid_css,
    backup=True
)

print(result)


print("\nFINAL CSS FILE")
print(TEST_CSS.read_text(encoding="utf-8"))