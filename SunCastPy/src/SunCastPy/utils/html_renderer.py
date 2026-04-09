from SunCastPy.Forecast.Base_Forecast import Forecast
from SunCastPy.utils.utils import format_hour


def render_html(grouped_data: dict[str, list[Forecast]]) -> str:
    """Generate a simple HTML page from grouped forecast data."""

    html_parts: list[str] = []

    html_parts.append("""
    <html>
    <head>
        <title>SunCast Forecast</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #0f172a;
                color: #e2e8f0;
                padding: 20px;
            }
            h1 {
                text-align: center;
            }
            .day {
                margin-bottom: 20px;
                padding: 15px;
                border-radius: 10px;
                background: #1e293b;
            }
            .forecast {
                margin-left: 10px;
                padding: 5px 0;
                border-bottom: 1px solid #334155;
            }
        </style>
    </head>
    <body>
        <h1>🌤 SunCast Forecast</h1>
    """)

    for day, forecasts in grouped_data.items():
        html_parts.append(f'<div class="day"><h2>{day}</h2>')

        for f in forecasts:
            html_parts.append(f"""
                <div class="forecast">
                    <img src="{f.image_url}" width="80">
                    <strong>{format_hour(f.start_time)} - {format_hour(f.end_time)}</strong><br>
                    Temp: {f.temperature}°{f.temperature_unit}<br>
                    Wind: {f.wind_speed} {f.wind_direction}<br>
                    {f.short_forecast}
                </div>
            """)

        html_parts.append("</div>")

    html_parts.append("""
    </body>
    </html>
    """)

    return "".join(html_parts)
