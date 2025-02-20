import dspy
import pandas as pd



# Configure the language model
dspy.configure(lm=dspy.LM('mistral/open-mistral-7b', api_key='QEhd2LOvC1OsJm5BYlj0wfjP89VMj9iK', temperature=0.1))

class Outline(dspy.Signature):
    """You're an agent which takes a text or template as input and generates the Outline for a report
        Generate list of sections
        Generate sections sub headings
        """

    template: str = dspy.InputField()
    title: str = dspy.InputField()
    sections: list[str] = dspy.OutputField()
    section_subheadings: dict[str, list[str]] = dspy.OutputField(desc="mapping from section headings to subheadings")

class DraftSection(dspy.Signature):
    """Draft a top-level section of a report.
    """

    title: str = dspy.InputField()
    section_heading: str = dspy.InputField()
    section_subheadings: list[str] = dspy.InputField()
    dataset = dspy.InputField()
    content: str = dspy.OutputField(desc="markdown-formatted section")

class DraftReport(dspy.Module):
    """Draft a report using the provided Outline & DraftSection"""
    def __init__(self):
        self.build_outline = dspy.ChainOfThought(Outline)
        self.draft_section = dspy.ChainOfThought(DraftSection)

    def forward(self, template,title,dataset):
        outline = self.build_outline(template=template,title=title)
        sections = []
        for heading, subheadings in outline.section_subheadings.items():
            section, subheadings = f"## {heading}", [f"### {subheading}" for subheading in subheadings]
            section = self.draft_section(title=title, section_heading=section, section_subheadings=subheadings, dataset=dataset)
            sections.append(section.content)
        return dspy.Prediction(title=title, sections=sections)

# Function to extract table metadata
def extract_table_metadata(df):
    metadata = {
        'column_names': df.columns.tolist(),
        'data_types': df.dtypes.to_dict(),
        'row_count': df.shape,
        'column_count': df.shape[1],
    }
    return metadata


# def read_word_doc(file_path):
#     return getdocumenttext(file_path)
        

def read_excel_file(file_path):
    try:
        df = pd.read_excel(file_path)
        return df
    except:
        print(f"Error reading Excel file:")
        return None


# Main function
def main():
    excel_file_path = 'learn-dspy/CVI_1YRCLOSEDINC.xlsx'
    word_file_path = 'RCA_Template.docx'

    # doc = read_word_doc(word_file_path)
    doc = """
    Root Cause Analysis
    Overview
    Problem Statement
    Incident Details
    Root Cause Identification
    Analysis of Causes
    Corrective Actions and Preventive Measures
    Impact Analysis
    Lessons Learned and Continuous Improvement
    Documentation and Communication
    Appendices
    """
    title = "Root cause analysis"
    df = read_excel_file(excel_file_path)
   
    if df is not None:
        metadata = extract_table_metadata(df)
        # print("Table Metadata:")
        # print(metadata)
        
        # Generate a article using DSPy
        draft_article = DraftReport()
        article = draft_article(template=doc,title=title,dataset=df)
        print("Generated Article :")
        print(article)
        
draft_article = DraftReport()
def genReport(data,template,title):
    
    article = draft_article(template=template,title=title,dataset=data)
    return article

if __name__ == "__main__":
    main()