import requests
import pandas as pd
import plotly.express as px

# Chamando a API
url = "https://api.github.com/search/repositories"
url += "?q=language:python+sort:stars+stars:>10000" 

headers = {"Accept": "application/vnd.github.v3+json"}

r = requests.get(url, headers=headers)
response_dict = r.json()
repo_dicts = response_dict["items"]

print("Status code:", r.status_code)
print("Complete results:", not response_dict["incomplete_results"])

df = pd.DataFrame(repo_dicts)
print(df.head())

# Filtrando os dados da API
repo_name, repo_stars, hover_texts = [], [], []

for repo in repo_dicts:
    repo_name.append(f"<a href='{repo['html_url']}' style='color:#000;'>{repo['name']}</a>")
    repo_stars.append(repo["stargazers_count"])

    description = repo["description"] or "Sem descrição"

    hover_text = (f"{repo['owner']['login']}<br>{description}")
    hover_texts.append(hover_text)

# Executando o plotly com os dados
title = "Projetos em Python com mais de 10k estrelas no GitHub"
labels = {"x": "Repositórios", "y": "Estrelas"}

fig = px.bar(
    x=repo_name,
    y=repo_stars,
    title=title,
    labels=labels,
    hover_name=hover_texts,
    template="seaborn"
)

fig.update_layout(title_font_size=28, xaxis_title_font_size=20, yaxis_title_font_size=20)
fig.update_traces(marker_color="steelblue", marker_opacity=0.6)

fig.show()