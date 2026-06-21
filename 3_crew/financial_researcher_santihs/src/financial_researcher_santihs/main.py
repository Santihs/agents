#!/usr/bin/env python
import warnings

from datetime import datetime

from financial_researcher_santihs.crew import FinancialResearcherSantihs

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the financial researcher crew.
    """
    inputs = {
        'company': 'Infios'
    }

    try:
        result =FinancialResearcherSantihs().crew().kickoff(inputs=inputs)
        print(result.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

if __name__ == "__main__":
    run()