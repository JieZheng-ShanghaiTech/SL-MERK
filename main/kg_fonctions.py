import requests
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()
API_BASE = str(os.getenv("API_BASE"))
API_KEY = str(os.getenv("API_KEY"))


def generate_with_graphrag(query,mode):
    command = ['python', '-m', 'graphrag.query', '--root', './NexLeth_GraphRAG','--method',f'{mode}', query]
    result = subprocess.run(command, capture_output=True, text=True)
    explanation = result.stdout.split('Global Search Response: ')[-1]
    return explanation

def generate(query, model):
    api_base = API_BASE  # replace with your API base URL
    api_key = API_KEY  # replace with your API key

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,  
        "messages": [
            {"role": "user", "content": query}  
        ],  
    }

    response = requests.post(api_base, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        ans = result['choices'][0]['message']['content']
        return ans
    else:
        print(f"请求失败，状态码: {response.status_code}")
        print("详细信息:", response.text)
        
def get_neighbors_by_relation(G, node, relation=None):
    if relation is None:
        return list(G.neighbors(node))
    else:
        neighbors = []
        for neighbor in G.neighbors(node):
            if (G[node][neighbor].get('label') in relation):
                neighbors.append(neighbor)
        return neighbors
    
def extract_bp_pw(G, head=None, tail=None):
    if tail == None:
        BP = get_neighbors_by_relation(G, node=head, relation=['PARTICIPATES_GpBP'])
        PW = get_neighbors_by_relation(G, node=head, relation=['PARTICIPATES_GpPW'])
        return BP, PW
    if head == None:
        BP = get_neighbors_by_relation(G, node=tail, relation=['PARTICIPATES_GpBP'])
        PW = get_neighbors_by_relation(G, node=tail, relation=['PARTICIPATES_GpPW'])
        return BP, PW
    SL_neighbors = get_neighbors_by_relation(G, node=head, relation=['SL_GsG'])
    neighbors_bp = set()
    neighbors_pw = set()
    for neighbor in SL_neighbors:
        BP_neighbors = get_neighbors_by_relation(G, node=neighbor, relation=['PARTICIPATES_GpBP'])
        PW_neighbors = get_neighbors_by_relation(G, node=neighbor, relation=['PARTICIPATES_GpPW'])
        neighbors_bp.update(BP_neighbors)
        neighbors_pw.update(PW_neighbors)
    BP_tail = get_neighbors_by_relation(G, node=tail, relation=['PARTICIPATES_GpBP'])
    PW_tail = get_neighbors_by_relation(G, node=tail, relation=['PARTICIPATES_GpPW'])
    BP = neighbors_bp.intersection(BP_tail)
    PW = neighbors_pw.intersection(PW_tail)
    return BP, PW

