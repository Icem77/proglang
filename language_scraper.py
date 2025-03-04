from duckduckgo_search import DDGS
from ranking_scraper import basic_info_scrape

def duckduckgo_description(language : str):
    description = "## Language description: \n"
    
    with DDGS() as ddgs:
        result = ddgs.text(f"{language} programming language description", max_results=1)
        
        if result:
            description += result[0].get("body", "No description found")
        else:
            description += "No description found."

    return description + "\n"

def duckduckgo_tutorials(language : str):

    string_result = "## Tutorials:\n"

    with DDGS() as ddgs:
        results = ddgs.text(f"{language} programing language tutorial", max_results=5)
        
        for idx, result in enumerate(results, start=1):
            title = result.get("title", "No Title")
            link = result.get("href", "No Link")
            string_result += f"* {title}:\n [visit tutorial no.{idx}]({link})\n"

    return string_result

def duckduckgo_memes(language : str):
    string_memes = "## Memes: \n"
    
    with DDGS() as ddgs:
        results = ddgs.images(f"{language} programming language memes", max_results=3)

        for idx, result in enumerate(results, start=1):
            image_url = result.get("image")
            string_memes += f"* ![{language} meme {idx}]({image_url}){{: style='width:300px; height:auto;' }}\n\n"

    return string_memes

def duckduckgo_documentation_link(language : str):

    string_documentation = "## Documentation: "

    with DDGS() as ddgs:
        results = ddgs.text(f"{language} programming language documentation", max_results=1)
        
        if results:
            string_documentation += f"[check {language} documentation]({results[0].get('href', 'No link found.')})\n"
        else:
            string_documentation += "No documentation found.\n"

    return string_documentation

def generate_post_for_language(date : str, language : str, image : str):
    print(f"GENERATING POST FOR: {language}\n")
    with open(f"_posts/{date}-{language}-post.md", "w") as file:
        file.write(f"---\nlayout: post\ntitle: '{language}'\n---\n")
        file.write(f"# Logo: ![logo]({image})\n\n")
        file.write(duckduckgo_description(language))
        file.write("\n")
        file.write(duckduckgo_documentation_link(language))
        file.write("\n")
        file.write(duckduckgo_tutorials(language))
        file.write("\n")
        file.write(duckduckgo_memes(language))

def generate_posts(date : str):
    data = basic_info_scrape()

    for item in data:
        generate_post_for_language(date, item["language"].replace(" ", "-").replace("/", "-"), item["logo"])

if __name__ == "__main__":
    generate_posts("2025-03-03")