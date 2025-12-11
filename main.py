from pathlib import Path 
from parser.parser import parse_strategy  
from codegen.generator import generate_python  
from backtest.simulator import generate_sample_prices, simulate  

def main():
    
    # 1. Load DSL

    dsl_path = Path("examples/basic_strategy.dsl")
    dsl_text = dsl_path.read_text() 

    print(dsl_text)

    # 2. DSL -> AST

    ast = parse_strategy(dsl_text)

    print(ast)

    # 3. AST -> Python

    python_code = generate_python(ast)
    print(python_code)

    # 4. Create sample price data

    sample_data = generate_sample_prices(20)
    for bar in sample_data[:3]:  
        print(bar)

    # 5. Backtest simulation

    result = simulate(sample_data)
    print(result)

if __name__ == "__main__":
    main()