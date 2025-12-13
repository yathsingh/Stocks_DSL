<h5>End-to-end NLP → DSL → AST → Python pipeline for stock trading strategies with backtesting.<h5>

Grammar explaination for better understanding: syntax_explaination.md 

Actual grammar syntax: dsl/syntax.md

<br><br>
**HOW TO RUN**

1. Clone the repo
   
2. Run main.py

You will have the options to pick preset language commands for testing
and quick report generation, of enter your own custom input.

*If you DO choose to enter custom input, please read:*

***Basic Rules***

Write one trading condition per sentence.

Do not use and / or within the same sentence.

If your strategy has multiple conditions, write them as multiple lines.

Clearly indicate whether a sentence is for entry (buy, enter) or exit (exit, sell).

Keep sentences short and direct.

***Examples***

1. Price vs Indicator

Buy when close is above the 20-day moving average.

2. Indicator vs Number

Exit when RSI 14 is below 30.

3. Volume Conditions

Buy when volume is above 1M.
Exit when volume is below 900k.

4. Cross Events

Enter when close crosses above the 10-day moving average.
Exit when close crosses below the 10-day moving average.

5. Lookback References

Buy when yesterday's high is above today's close.

<br><br>
**(EXTRA)**
**DOCUMENTATION OF BUILDING PROCESS:**

Phase 1 => Skeleton 
1. Created a base 'template' architecture of folders.
2. Created a basic tokenizer to call as a placeholder.
3. Defined AST nodes.
4. Mock parser and generator to test AST -> Python code pipeline.
5. Create basic simulator for OHLC values and processing them.
6. Created prototype main.py and confirmed pipeline working.

Phase 2 => DSL
1. Defined and locked syntax.
2. Defined valid indicators.
3. Defined operators.
4. Created tokenizer.

Phase 3 => Parser
1. Created AST Nodes.
2. Created token stream (parser helper).
3. Created parser.

Phase 4 => Generator
1. Created generator.

Phase 5 => Backtest
1. Created simulator.

Phase 6 => NLP
1. Created Natural Language to JSON Structure converter.
2. Created JSON Structure to DSL converter.

Phase 7 => Backtest (v2) 
1. Created main function to showcase pipeline.
2. Polished the pipeline components and improved main function for demos.
