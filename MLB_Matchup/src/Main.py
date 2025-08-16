import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Xbot'))

from MLBMatchup import MLBMatchup

"""
params: None
returns: int - Exit code (0 for success, 1 for error)
summary: Main entry point that orchestrates the MLB game processing workflow
"""
def MainCommand():
    try:
        orchestrator = MLBMatchup()
        result = orchestrator.process_games()
        
        if result == "ALL_DONE":
            return 0
        else:
            return 0
            
    except Exception as e:
        print(f"Error in main execution: {e}")
        return 1


if __name__ == "__main__":
    exit(MainCommand())