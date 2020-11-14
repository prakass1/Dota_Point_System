import points_calculation as pc
import buff_extraction as be

# Start of main
if __name__ == "__main__":
    # Get the data from dotabuff first
    player_game_data = be.main_process()
    total_points_data = pc.calculate_points(player_game_data)
    pc.write_template(total_points_data)
    print("Completed writing the ranking in html folder. Please check it")
