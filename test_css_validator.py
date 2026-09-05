from backend.services.css_validator import validate_css


valid_css = """
@media (max-width: 768px) {
    .navbar-nav {
        flex-direction: column;
    }
}
"""

invalid_html = """
<div class="navbar">
    Test
</div>
"""

invalid_js = """
document.querySelector('.navbar');
"""


print("VALID CSS TEST:")
print(validate_css(valid_css))

print("\nHTML TEST:")
print(validate_css(invalid_html))

print("\nJAVASCRIPT TEST:")
print(validate_css(invalid_js))