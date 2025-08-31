# SL-MERK
SL-MERK is an explainable AI method for generating natural language explanation of synthetic lethality (SL) mechanisms based on LLMs and GraphRAG.

## Features

- **Multiple Analysis Modes**:
  - **KG Mode**: Leverages a knowledge graph to explain synthetic lethality mechanisms
  - **GraphRAG Mode**: Uses graph-based retrieval-augmented generation with global or local context
  - **Merged Mode**: Combines both KG and GraphRAG approaches for comprehensive explanations

- **Flexible Query Options**:
  - Analyze specific gene pairs
  - Ask free-form questions about synthetic lethality mechanisms
  
- **Model Compatibility**:
  - Works with various large language models
  - Customizable model selection

## Installation

```bash
git clone https://github.com/JieZheng-ShanghaiTech/SL-MERK.git
cd SL-MERK
pip install -r requirements.txt
```

## Configuration

**Important:** Before using this tool, you need to configure your API credentials:

1. Create a `.env` file in the root directory
2. Add your API base URL and key:
   ```
   API_BASE=your_api_base_url_here
   API_KEY=your_api_key_here
   ```

Alternatively, you can set these as environment variables in your system.
3. Remember to configure the Graph/NexLeth_GraphRAG/setting.yaml, set your api_base and api_key for GraphRAG, and you can chose the models and change detailed settings.

## Dependencies

- networkx
- argparse
- (Other dependencies as specified in requirements.txt)

## Usage

### Command Line Interface

```bash
python main.py --mode [kg|graphrag|merged] --graphrag-mode [global|local] --model [model_name]
```

### Interactive Mode

Simply run the script without arguments for an interactive session:

```bash
python main.py
```

The tool will guide you through selecting:
1. Operation mode (KG, GraphRAG, or Merged)
2. GraphRAG mode (Global or Local)
3. Language model to use
4. Gene pair information or query text

### Examples

#### Knowledge Graph Mode

```bash
python main.py --mode kg --model gpt-4
```

#### GraphRAG Mode

```bash
python main.py --mode graphrag --graphrag-mode global --model claude-3
```

#### Merged Mode

```bash
python main.py --mode merged --graphrag-mode local --model gpt-4
```

## API Usage

You can also use the functions directly in your Python code:

```python
from main import get_resultOfKg, get_resultOfGraphrag, get_merged_result

# Using KG mode
kg_explanation = get_resultOfKg(gene_pair=('BRCA1', 'PARP1'), model='gpt-4')

# Using GraphRAG mode
graphrag_explanation = get_resultOfGraphrag(
    query="Explain the synthetic lethality mechanism between BRCA1 and PARP1",
    mode='global'
)

# Using merged mode
merged_explanation = get_merged_result(
    query=None,
    gene_pair=('BRCA1', 'PARP1'),
    model='gpt-4',
    graphrag_mode='global'
)
```

## Data

The tool uses a synthetic lethality knowledge graph stored in GraphML format. The default path is:

```
data/synlethKG/synlethKG.graphml
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).

## Citation

If you use this tool in your research, please cite:

```
@software{SynLethKG,
  author = {Your Name},
  title = {SL-MERK: Synthetic Lethality Mechanism Explainer based on GraphRAG and Knowledge Graph},
  year = {2025},
  url = {https://github.com/JieZheng-ShanghaiTech/SL-MERK}
}
```
