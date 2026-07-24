from SunCastPy.utils.html_renderer import render_html, render_index


def test_render_index_contains_locations():
    locations = [
        {"name": "San Juan"},
        {"name": "Mayaguez"},
    ]

    html = render_index(locations)

    assert "San Juan" in html
    assert "Mayaguez" in html


def test_render_html_contains_location():
    grouped_data = {"Monday": []}

    html = render_html(
        grouped_data,
        "Mayaguez",
        "forecast.html.j2",
    )

    assert "Mayaguez" in html
