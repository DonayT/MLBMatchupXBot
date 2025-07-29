import schedule
import time
import subprocess
import sys
import logging
from datetime import datetime
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mlb_scheduler.log'),
        logging.StreamHandler()
    ]
)

def run_mlb_script():
    """Run the MLB matchup script with detailed logging"""
    try:
        logging.info("🕐 Starting MLB script execution...")
        
        # Run the script
        result = subprocess.run(
            [sys.executable, 'MLBMatchup.py'], 
            capture_output=True, 
            text=True,
            cwd=os.getcwd()  # Ensure we're in the right directory
        )
        
        if result.returncode == 0:
            logging.info("✅ MLB script completed successfully")
            if result.stdout.strip():
                logging.info(f"📤 Script output:\n{result.stdout}")
        else:
            logging.error("❌ MLB script failed")
            if result.stderr.strip():
                logging.error(f"📤 Error output:\n{result.stderr}")
                
    except Exception as e:
        logging.error(f"❌ Exception running MLB script: {e}")

def main():
    """Main scheduler with advanced features"""
    logging.info("🚀 Advanced MLB Lineup Scheduler Started!")
    logging.info("⏰ Will run every 15 minutes")
    logging.info("📝 Logs saved to: mlb_scheduler.log")
    logging.info("🛑 Press Ctrl+C to stop")
    logging.info("-" * 50)
    
    # Schedule the job to run every 15 minutes
    schedule.every(15).minutes.do(run_mlb_script)
    
    # Run immediately on startup
    logging.info("🎯 Running initial execution...")
    run_mlb_script()
    
    # Main loop
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
            
        except KeyboardInterrupt:
            logging.info("🛑 Scheduler stopped by user")
            break
        except Exception as e:
            logging.error(f"❌ Unexpected error in scheduler: {e}")
            time.sleep(60)  # Wait a minute before continuing

if __name__ == "__main__":
    main() 