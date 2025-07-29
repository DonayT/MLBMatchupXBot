import time
import subprocess
import sys
from datetime import datetime

def run_mlb_script():
    """Run the MLB matchup script"""
    try:
        print(f"\n🕐 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running MLB script...")
        result = subprocess.run([sys.executable, 'src/MLBMatchup.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Script completed successfully")
            if result.stdout:
                print("📤 Output:")
                print(result.stdout)
        else:
            print("❌ Script failed")
            if result.stderr:
                print("📤 Error:")
                print(result.stderr)
                
    except Exception as e:
        print(f"❌ Error running script: {e}")

def main():
    """Main scheduler loop"""
    print("🚀 MLB Lineup Scheduler Started!")
    print("⏰ Will run every 15 minutes")
    print("🛑 Press Ctrl+C to stop")
    print("-" * 50)
    
    # Run immediately on startup
    run_mlb_script()
    
    # Then run every 15 minutes
    while True:
        try:
            # Wait 15 minutes (900 seconds)
            print(f"⏳ Waiting 15 minutes until next run...")
            time.sleep(900)
            run_mlb_script()
            
        except KeyboardInterrupt:
            print("\n🛑 Scheduler stopped by user")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            print("🔄 Continuing in 15 minutes...")
            time.sleep(900)

if __name__ == "__main__":
    main() 