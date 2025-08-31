import networkx as nx
import os
import argparse
from kg_fonctions import generate, generate_with_graphrag
from kg_prompt import prompt_merge_explanation
from kg_explainer import explain_with_kg


def get_resultOfGraphrag(query=None,gene_pair=None,mode='global'):
    mode = 'global' if mode not in ['global','local'] else mode
    if query is None and gene_pair is not None:
        query = f'Explain the synthetic lethality mechanism between {gene_pair[0]} and {gene_pair[1]}, please provide only the explanation of the mechanism. Keep it as concise as possible while including key information.'
    if query is None and gene_pair is None:
        raise ValueError("Either query or gene_pair must be provided.")
    result = generate_with_graphrag(query,mode)
    return result


def get_resultOfKg(gene_pair,model):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    graph_path = os.path.join(script_dir, '../data/synlethKG/synlethKG.graphml')
    graph_path = os.path.normpath(graph_path)

    # 使用绝对路径加载文件
    kg = nx.read_graphml(graph_path)
    result = explain_with_kg(kg, gene_pair[0], gene_pair[1], model=model)
    return  result 

def get_merged_result(query,gene_pair,model,graphrag_mode='global'):
    result_kg = get_resultOfKg(gene_pair,model)
    result_graphrag = get_resultOfGraphrag(query,graphrag_mode)
    query = prompt_merge_explanation.format(geneA=gene_pair[0], geneB=gene_pair[1], explanation_kg=result_kg, explanation_graphrag=result_graphrag)
    result = generate(query,model)
    return result

def main():
    # 设置命令行参数解析器
    parser = argparse.ArgumentParser(description='Graph analysis tool with multiple modes')
    parser.add_argument('--mode', choices=['kg', 'graphrag', 'merged'], 
                      help='Choose the operation mode: kg, graphrag, or merged')
    parser.add_argument('--graphrag-mode', choices=['global', 'local'], 
                      help='GraphRAG mode: global or local')
    parser.add_argument('--model', help='Name of the large language model to use')
    
    # 解析已知的命令行参数
    args, unknown = parser.parse_known_args()
    
    # 如果未提供模式，提示用户选择
    if not args.mode:
        print("请选择运行模式:")
        print("1. 仅使用KG (get_resultOfKg)")
        print("2. 仅使用GraphRAG (get_resultOfGraphrag)")
        print("3. 使用合并结果 (get_merged_result)")
        
        while True:
            choice = input("请输入选项 (1/2/3): ").strip()
            if choice in ['1', '2', '3']:
                args.mode = ['kg', 'graphrag', 'merged'][int(choice)-1]
                break
            print("无效选项，请重试")
    
    # 获取graphrag模式
    if not args.graphrag_mode:
        print("\n请选择GraphRAG模式:")
        print("1. global")
        print("2. local")
        
        while True:
            choice = input("请输入选项 (1/2): ").strip()
            if choice in ['1', '2']:
                args.graphrag_mode = ['global', 'local'][int(choice)-1]
                break
            print("无效选项，请重试")
    
    # 获取模型名称
    if not args.model:
        args.model = input("\n请输入要使用的大语言模型型号: ").strip()
        while not args.model:
            args.model = input("模型型号不能为空，请重新输入: ").strip()
    
    # 根据模式获取必要的参数
    gene_pair = None
    query = None
    
    if args.mode in ['kg', 'merged']:
        # 需要gene_pair
        print("\n请输入基因对信息")
        geneA = input("请输入geneA: ").strip()
        while not geneA:
            geneA = input("geneA不能为空，请重新输入: ").strip()
            
        geneB = input("请输入geneB: ").strip()
        while not geneB:
            geneB = input("geneB不能为空，请重新输入: ").strip()
            
        gene_pair = (geneA, geneB)
    
    if args.mode == 'graphrag' and gene_pair is None:
        # 如果是graphrag模式且没有gene_pair，则需要query
        query = input("\n请输入查询内容: ").strip()
        while not query:
            query = input("查询内容不能为空，请重新输入: ").strip()
    
    # 执行相应的函数并输出结果
    print("\n正在处理，请稍候...\n")
    
    try:
        if args.mode == 'kg':
            result = get_resultOfKg(gene_pair, args.model)
        elif args.mode == 'graphrag':
            result = get_resultOfGraphrag(query, gene_pair, args.graphrag_mode)
        else:  # merged
            result = get_merged_result(query, gene_pair, args.model, args.graphrag_mode)
        
        print("结果:")
        print("=" * 50)
        print(result)
        print("=" * 50)
        
    except Exception as e:
        print(f"处理过程中发生错误: {str(e)}")


if __name__ == "__main__":
    main()
