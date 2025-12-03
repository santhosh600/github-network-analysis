"""
Setup Mode: GitHub Network Analysis for santhosh600

- Checks for required packages and installs them if missing
- Prompts user for GitHub Personal Access Token (if not set)
- Fetches all public repos for 'santhosh600'
- Pulls and visualizes contributor-repository network

First-time users: just run this file after adding it to your repo.

Requirements: Python >= 3.7
"""

import sys
import subprocess

def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        __import__(package)

for pkg in ["requests", "networkx", "matplotlib"]:
    install_and_import(pkg)

import requests
import networkx as nx
import matplotlib.pyplot as plt
import os

USER = "santhosh600"

def get_github_token():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        token = input("Enter your GitHub Personal Access Token: ").strip()
        os.environ["GITHUB_TOKEN"] = token
    return token

GITHUB_TOKEN = get_github_token()
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

def fetch_repos(user):
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{user}/repos?per_page=100&page={page}"
        resp = requests.get(url, headers=HEADERS)
        if resp.status_code != 200:
            print(f"Error fetching repos: {resp.status_code}")
            break
        data = resp.json()
        if not data:
            break
        for repo in data:
            repos.append(repo["full_name"])
        page += 1
    return repos

def fetch_contributors(repo):
    url = f"https://api.github.com/repos/{repo}/contributors"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        return [user["login"] for user in resp.json()]
    else:
        print(f"Error fetching contributors for {repo}: {resp.status_code}")
        return []

def build_network(repos):
    G = nx.Graph()
    for repo in repos:
        G.add_node(f"repo:{repo}", bipartite="repo")
        contributors = fetch_contributors(repo)
        for user in contributors:
            G.add_node(f"user:{user}", bipartite="user")
            G.add_edge(f"user:{user}", f"repo:{repo}")
    return G

def analyze_and_visualize(G):
    centrality = nx.degree_centrality(G)
    print("Degree Centrality (Top 10):")
    print(sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10])

    plt.figure(figsize=(10,7))
    repo_nodes = [n for n in G.nodes if n.startswith("repo:")]
    user_nodes = [n for n in G.nodes if n.startswith("user:")]
    pos = nx.spring_layout(G, k=0.5)
    nx.draw_networkx_nodes(G, pos, nodelist=repo_nodes, node_color="blue", node_size=300, label="Repos")
    nx.draw_networkx_nodes(G, pos, nodelist=user_nodes, node_color="red", node_size=100, label="Users")
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos, font_size=8)
    plt.legend()
    plt.title("GitHub Contributor Network for santhosh600")
    plt.axis("off")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    all_repos = fetch_repos(USER)
    print(f"Found {len(all_repos)} repositories for {USER}:")
    for r in all_repos:
        print(" ", r)
    G = build_network(all_repos)
    analyze_and_visualize(G)
