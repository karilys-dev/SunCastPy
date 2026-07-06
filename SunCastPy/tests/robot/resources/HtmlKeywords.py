# mypy: ignore-errors
# pylint: skip-file
from pathlib import Path
from bs4 import BeautifulSoup


class HtmlKeywords:
    def load_html(self, html_file):
        html = Path(html_file).read_text(encoding="utf-8")
        return BeautifulSoup(html, "html.parser")

    def page_title_should_be(self, soup, expected):
        h1 = soup.find("h1")
        assert h1 is not None
        assert h1.text.strip() == expected

    def city_should_be(self, soup, expected, index=0):
        h2 = soup.find_all("h2")[index]
        assert expected in h2.text.strip()

    def page_should_have_forecast(self, soup):
        day = soup.find("div", class_="day")
        assert day is not None
        table = day.find("table")
        assert table is not None

        rows = table.find_all("tr")
        assert len(rows) > 0

        for row in rows:
            img = row.find("img")
            assert img is not None
            assert img.get("src")
            assert img.get("alt")

            forecast = row.find("div", class_="forecast")
            assert forecast is not None

    def forecast_day_limit_should_be(self, soup, limit):
        day = soup.find_all("div", class_="day")
        assert len(day) == int(limit), f"The actual value was {len(day)}"

    def get_forecast_row_count(self, file):
        soup = self.load_html(html_file=file)
        day = soup.find("div", class_="day")
        assert day is not None
        table = day.find("table")
        assert table is not None

        rows = table.find_all("tr")
        return len(rows)
