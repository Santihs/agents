#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime

from stock_picker.crew import StockPicker

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the research crew.
    """
    run_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    os.makedirs(f"output/{run_timestamp}", exist_ok=True)

    inputs = {
        'sector': os.getenv('SECTOR', 'Technology'),
        'current_date': str(datetime.now()),
        'run_timestamp': run_timestamp,
    }

    # Create and run the crew
    result = StockPicker().crew().kickoff(inputs=inputs)

    # Print the result
    print("\n\n=== FINAL DECISION ===\n\n")
    print(result.raw)


if __name__ == "__main__":
    run()
