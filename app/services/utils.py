def is_linkedin_url(url):
    return url.startswith("https://www.linkedin.com/in/")

def extrair_nome(linkedin_url):
    return linkedin_url.rstrip('/').split("/")[-1].replace("-", " ").title()
