from edgar import Company, TXTML
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken


def get_cik_from_ticker(ticker):
    url = "https://www.sec.gov/include/ticker.txt"
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        content = response.text

        # Split the content by lines and then split each line by tabs
        lines = content.strip().split('\n')
        ticker_cik_dict = {line.split('\t')[0]: line.split('\t')[1] for line in lines}

        # Get the CIK from the dictionary using the ticker
        cik = ticker_cik_dict.get(ticker.lower(), "Ticker not found")
        return cik

    else:
        print(f"Error: {response.status_code}")
        return None
    
def get_10k_filing_text_cik(cik):
    # Initialize a Company object with the given CIK
    company = Company("", cik)

    # Get the latest 10-K filing
    doc = company.get_10K()

    # Parse the full 10-K filing as text
    text = TXTML.parse_full_10K(doc)

    return text

def get_10q_filing_text_cik(cik):
    # Initialize a Company object with the given CIK
    company = Company("", cik)

    # Get the latest 10-Q filing
    doc = company.get_10Qs(no_of_documents=1, as_documents=True)[0]

    # Parse the full 10-Q filing as text
    text = TXTML.parse_full_10K(doc)

    return text
def get_10q_filing_text_tick(ticker):
    # Get the CIK from the ticker
    cik = get_cik_from_ticker(ticker)

    # Get the 10-Q filing text from the CIK
    text = get_10q_filing_text_cik(cik)

    return text

def get_10k_filing_text_tick(ticker):
    # Get the CIK from the ticker
    cik = get_cik_from_ticker(ticker)

    # Get the 10-K filing text from the CIK
    text = get_10k_filing_text_cik(cik)

    return text


tokenizer = tiktoken.get_encoding('cl100k_base')

# create the length function
def tiktoken_len(text):
    tokens = tokenizer.encode(
        text,
        disallowed_special=()
    )
    return len(tokens)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=20,  # number of tokens overlap between chunks
    length_function=tiktoken_len,
    separators=['\n\n', '\n', ' ', '']
)






import openai
openai.api_key = "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"  #platform.openai.com



def get_chunk_summary(chunk):
    primer = f"""You are a financial analyst at a hedge fund. You are tasked with analyzing the financial performance of a company and providing a concise summary of your findings. You are given a segment of a 10k financial report and are asked to provide key insights about the company's performance."""
    query = """Analyze the following segment from a 10k financial report and provide concise notes highlighting key insights about the company's performance. Focus on significant details that will help determine whether or not to invest in the company. Please structure your output notes as bullet points under the following categories: Revenue & Profitability, Expenses & Liabilities, Growth & Market Position, Risks & Challenges, and Management & Strategy. The input segment is as follows:

    [""" + chunk + """"]

    Provide key insights under the appropriate categories below:

    Revenue & Profitability:
    -
    Expenses & Liabilities:
    -
    Growth & Market Position:
    -
    Risks & Challenges:
    -
    Management & Strategy:
    -
    """


    res = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": primer},
            {"role": "user", "content": query}
        ],
        temperature=0.3, 
        max_tokens=1700,
        top_p=1, 
        frequency_penalty=0,
        presence_penalty=1
    )
    return (res['choices'][0]['message']['content'])





def consolidate_notes(notes_list):
    consolidated_notes = {
        "Revenue & Profitability:": [],
        "Expenses & Liabilities:": [],
        "Growth & Market Position:": [],
        "Risks & Challenges:": [],
        "Management & Strategy:": [],
    }

    for note in notes_list:
        lines = note.split("\n")
        current_section = None
        for line in lines:
            if line.startswith("- "):
                consolidated_notes[current_section].append(line)
            elif line.strip() in consolidated_notes:
                current_section = line.strip()

    result = ""
    for section, bullet_points in consolidated_notes.items():
        result += f"{section}:\n"
        for bullet in bullet_points:
            result += bullet + "\n"
        result += "\n"
    return result


def full_summary(text):
    chunks = text_splitter.split_text(text)
    summaries = []
   
    print("Analizing "+str(len(chunks))+" chunks")
    for chunk in chunks:
        try:
            summaries.append(get_chunk_summary(chunk))
        except:
            try:
                summaries.append(get_chunk_summary(chunk))
            except:
                continue
    
    return consolidate_notes(summaries)


def string_to_file(text, filename):
    with open(filename, "w") as f:
        f.write(text)
        f.close()


def ticker_to_file(ticker):
    text = get_10k_filing_text_tick(ticker)
    summ = full_summary(text)
    print(summ)
    string_to_file(summ, ticker+"-GPT-Notes.txt")





ticker_to_file("msft")



