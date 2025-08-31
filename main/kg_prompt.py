

prompt_SummarizeGeneFunction = """
Please summarize the functional characteristics of the gene based on the provided relevant biological processes and pathways.
For the biological processes and pathways related to cancer, more emphasis and details can be retained.
If two gene names are provided, please summarize the provided biological processes and pathways as the functions that the two genes may participate in together,
and also highlight the cancer-related content.
- gene name -
{gene}
- biological processes -
{bp}
- pathway -
{pw}
"""


prompt_ExplainMechanism = """
Explain the synthetic lethality mechanism between {geneA} and {geneB} based on provided information, 
please provide only the explanation of the mechanism. Keep it as concise as possible while including key information.

- functions of {geneA} -
{function_geneA}

- functions of {geneB} -
{function_geneB}

- functions shared between {geneA} and {geneB} -
{function_shared}
"""


prompt_merge_explanation = """
Based on the following two explanations of the synthetic lethality mechanism between {geneA} and {geneB}, 
please merge them into a single, concise explanation that combines the strengths of both.
Ensure that the merged explanation is coherent, avoids redundancy, and retains all critical information from both sources.

- Explanation from Knowledge Graph-based method -{explanation_kg}

- Explanation from GraphRAG-based method -{explanation_graphrag}
"""