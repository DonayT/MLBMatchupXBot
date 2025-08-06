from MLB_API_Client import MLBAPIClient

def test_team_records():
    """Test the new team records functionality"""
    client = MLBAPIClient()
    
    print("Testing Team Records from MLBAPIClient:")
    print("=" * 50)
    
    # Get all team records
    all_records = client.get_team_records()
    print(f"Total teams found: {len(all_records)}")
    
    # Test getting specific team records
    test_teams = ["Boston Red Sox", "New York Yankees", "Los Angeles Dodgers"]
    
    for team in test_teams:
        record = client.get_team_record(team)
        print(f"{team}: {record['record']} ({record['wins']}W, {record['losses']}L)")
    
    print("=" * 50)

if __name__ == "__main__":
    test_twitter_image_with_records()