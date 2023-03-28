Financial Report Analyzer README
This script provides a set of functions to download and analyze the latest financial reports (10-K and 10-Q) of public companies from the US Securities and Exchange Commission (SEC). It uses the GPT-4 model to analyze the text and provide concise notes on key insights about the company's performance.

Dependencies
edgar - for downloading financial reports from the SEC
requests - for making HTTP requests
langchain.text_splitter - for splitting text into manageable chunks
tiktoken - for tokenizing text
openai - for using the GPT-4 model
Functions
get_cik_from_ticker(ticker): Given a stock ticker, returns the Central Index Key (CIK) of the company.
get_10k_filing_text_cik(cik): Given a CIK, returns the latest 10-K filing text of the company.
get_10q_filing_text_cik(cik): Given a CIK, returns the latest 10-Q filing text of the company.
get_10q_filing_text_tick(ticker): Given a stock ticker, returns the latest 10-Q filing text of the company.
get_10k_filing_text_tick(ticker): Given a stock ticker, returns the latest 10-K filing text of the company.
tiktoken_len(text): Returns the number of tokens in a given text.
get_chunk_summary(chunk): Analyzes a chunk of text from a financial report and returns a summary of key insights under pre-defined categories.
consolidate_notes(notes_list): Consolidates the summaries of all chunks into a single summary.
full_summary(text): Given the text of a financial report, returns the full summary of key insights.
string_to_file(text, filename): Writes a given text to a file with a specified filename.
ticker_to_file(ticker): Given a stock ticker, writes the summary of the latest 10-K filing text to a file.
Usage
To generate a summary of the latest 10-K filing for a company, use the ticker_to_file function with the stock ticker as an argument:


ticker_to_file("msft")


This will create a file named msft-GPT-Notes.txt containing the summary of the latest 10-K filing for Microsoft Corporation.



