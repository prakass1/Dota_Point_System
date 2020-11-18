import points_calculation as pc
import buff_extraction as be
import properties

# Start of main
if __name__ == "__main__":
    # Get the data from dotabuff first
    properties.match_ids = be.populate_match_ids()
    print(properties.match_ids)
    player_game_data = be.main_process()
    if player_game_data:
        total_points_data = pc.calculate_points(player_game_data)
        pc.write_template(total_points_data)
        print("Completed writing the ranking in html folder. Please check it")
    else:
        print("Perform manual intervention since could not fetch the match ids")
