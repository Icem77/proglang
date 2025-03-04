import requests
from bs4 import BeautifulSoup

def basic_info_scrape() -> dict:
    url = "https://www.tiobe.com/tiobe-index/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    language_info = []

    table_body = soup.find("table", {"class": "table table-striped table-top20"}).find("tbody")

    for row in table_body.find_all("tr"):
        data = row.find_all("td")
        language = data[4].text
        curr_year_rating = data[0].text
        prev_year_rating = data[1].text
        logo = "https://www.tiobe.com" + data[3].find("img").get("src")

        trend = "↑" 
        if data[0].text > data[1].text:
            trend = "↓"
        elif data[0].text == data[1].text:
            trend = "→"

        language_info.append({
            "language": language,
            "curr_year_rating": curr_year_rating,
            "prev_year_rating": prev_year_rating,
            "trend": trend,
            "logo": logo
        })

    return language_info

def write_ranking_to_markdown_file(data : dict):
    with open("ranking.md", "w") as file:
        file.write("---\nlayout: default\ntitle: 'Programming Languages Ranking (Top 20)'\npermalink: /\n---\n")
        file.write("# Programming Languages Ranking (Top 20)\n\n")

        for language in data:
            file.write(f"## {language['curr_year_rating']}. {language['language']} {{% capture my_post_url %}}{{% post_url 2025-03-03-{language['language'].replace(' ', '-').replace('/', '-')}-post %}}{{% endcapture %}}[more about {language['language']}]({{{{ my_post_url | relative_url }}}})\n" + 
                f"  * Popularity Trend: **{language['trend']}**\n" + 
                f"  * Previous Year Rating: **{language['prev_year_rating']}**\n" +
                f"  * Logo: ![Logo]({language['logo']})\n" +
                "\n"
            )

if __name__ == "__main__":
    write_ranking_to_markdown_file(basic_info_scrape())