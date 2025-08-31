import networkx as nx
import pandas as pd
from tqdm import tqdm
from kg_fonctions import generate, generate_with_graphrag, extract_bp_pw
from kg_prompt import prompt_SummarizeGeneFunction, prompt_ExplainMechanism


def generate_summary(gene, bp, pw, model):
    query=prompt_SummarizeGeneFunction.format(gene=gene,bp=bp,pw=pw)
    summary = generate(query, model)
    return summary



def explain_with_kg(kg, geneA, geneB, model):
    geneA_bp, geneA_pw = extract_bp_pw(kg, head=geneA)
    geneB_bp, geneB_pw = extract_bp_pw(kg, tail=geneB)
    shared_bp, shared_pw = extract_bp_pw(kg, head=geneA, tail=geneB)
    function_geneA = generate_summary(geneA, geneA_bp, geneA_pw, model=model)
    function_geneB = generate_summary(geneB, geneB_bp, geneB_pw, model=model)
    function_shared = generate_summary((geneA, geneB), shared_bp, shared_pw, model=model)
    
    query = prompt_ExplainMechanism.format(geneA=geneA, geneB=geneB, function_geneA=function_geneA, function_geneB=function_geneB, function_shared=function_shared)
    explanation = generate(query,model)
    return explanation  

def slrag_with_kgPrompt(kg, geneA, geneB, model, graphrag_mode='global'):
    mode = 'global' if graphrag_mode not in ['global','local'] else graphrag_mode
    geneA_bp, geneA_pw = extract_bp_pw(kg, head=geneA)
    geneB_bp, geneB_pw = extract_bp_pw(kg, tail=geneB)
    shared_bp, shared_pw = extract_bp_pw(kg, head=geneA, tail=geneB)
    function_geneA = generate_summary(geneA, geneA_bp, geneA_pw, model=model)
    function_geneB = generate_summary(geneB, geneB_bp, geneB_pw, model=model)
    function_shared = generate_summary((geneA, geneB), shared_bp, shared_pw, model=model)
    
    query = prompt_ExplainMechanism.format(geneA=geneA, geneB=geneB, function_geneA=function_geneA, function_geneB=function_geneB, function_shared=function_shared)
    explanation = generate_with_graphrag(query,mode)
    return explanation


if __name__ == '__main__':
    kg = nx.read_graphml("../data/synlethKG/synlethKG.graphml")
    df_label  = pd.read_csv("/SL_MERK/data/df_label.csv", index_col=0)
    results_df = pd.DataFrame(columns=['geneA','geneB','result'])
    for idx, row in tqdm(enumerate(df_label.iterrows())):
        result = explain_with_kg(kg, row[1].iloc[0], row[1].iloc[1], model='gpt-4o-mini')
        results_df.loc[idx] = [row[1].iloc[0],row[1].iloc[1],result]
        results_df.to_csv("/home/xuehenglv/SLRAG/results/df_results_kg_4omini.csv")
