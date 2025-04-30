import os
import requests
import webbrowser
import matplotlib.pyplot as plt

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/90.0.4430.85 Safari/537.36"
}

def fetch_archives(username):
    url = f"https://api.chess.com/pub/player/{username}/games/archives"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return data.get("archives", [])

def fetch_games_from_archive(archive_url):
    response = requests.get(archive_url, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return data.get("games", [])

def filter_games(games, username, threshold_lower, threshold_upper):
    urls = []
    for game in games:
        accuracies = game.get("accuracies")
        if not accuracies:
            continue

        white = game.get("white", {}).get("username", "").lower()
        black = game.get("black", {}).get("username", "").lower()

        if username.lower() == white:
            player_accuracy = accuracies.get("white", 0)
        elif username.lower() == black:
            player_accuracy = accuracies.get("black", 0)
        else:
            continue

        if player_accuracy >= threshold_lower and player_accuracy <= threshold_upper:
            url = game.get("url", "")
            if url:
                urls.append(url)
    return urls

def to_review_url(game_url):
    return game_url.replace("/game/", "/analysis/game/") + "?tab=review"

def save_urls_to_txt(urls, output_file):
    folder = os.path.dirname(output_file)
    os.makedirs(folder, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        for url in urls:
            f.write(url + "\n")

def categorizer(usernames):
    archives = []
    total_analyzed = 0

    for user in usernames:
        print(f"Fetching archives for {user}...")
        archives = fetch_archives(user)
        print(f"Found {len(archives)} archive links.\n")

        all_games = []
        for archive_url in archives:
            print(f"Fetching games from {archive_url}...")
            games = fetch_games_from_archive(archive_url)
            all_games.extend(games)
        print(f"Total games loaded: {len(all_games)}\n")

        threshold_lower = 95.0

        while threshold_lower > 0:
            threshold_upper = threshold_lower + 5.0
            print(f"Filtering games with accuracies between {threshold_lower}% and ≤ {threshold_upper}%...")
            game_urls = filter_games(all_games, user, threshold_lower, threshold_upper)
            total_analyzed = total_analyzed  + len(game_urls)
            print(f"Games found: {len(game_urls)}")

            final_urls = [to_review_url(url) for url in game_urls]

            if len(final_urls) > 0:
                print(f"Saving review URLs to {user + '/' + str(threshold_lower) + '-' + str(threshold_upper) + '.txt'}...\n")
                save_urls_to_txt(final_urls, "Records/" + user + '/' + str(threshold_lower) + "-" + str(threshold_upper) + '.txt')
            threshold_lower = threshold_lower - 5.0
        print(f"Finished processing for {user}.\n\n")
    print(f"Total games analyzed: {total_analyzed}\n")

def stats(usernames):
    accuracies = []
    accuracy_labels = []
    sum = 0
    mean = 0

    for i in range(20):
        games = 0
        lower = i * 5
        upper = (i + 1) * 5
        accuracy_labels.append(str((lower + upper)/2) + "%")
        for user in usernames:
            directory = "Records/" + user + "/"
            txt_file = os.path.join(directory, str(float(lower)) + "-" + str(float(upper)) + ".txt")
            if os.path.exists(txt_file):
                with open(txt_file, "r") as file:
                    games = games + len(file.readlines())
        accuracies.append(games)
        sum = sum + games
        mean = mean + games*(lower + upper)/2
    mean = mean / sum

    median_index = 0
    median_number = sum / 2
    while median_number > 0:
        median_number = median_number - accuracies[median_index]
        median_index += 1

    median = median_index * 5 + 2.5

    mode_frequencies = max(accuracies)
    mode_indices = [i for i, v in enumerate(accuracies) if v == mode_frequencies]
    modes = [i*5 + 2.5 for i in mode_indices]

    print(accuracies)
    print(f"Total games analyzed: {sum}")
    print(f"Mean accuracy: {mean:.2f}")
    print(f"Median accuracy: {median:.2f}")
    print(f"Mode accuracies: {modes}\n")

    plt.plot(accuracy_labels, accuracies, marker='o')
    plt.title("Accuracies Plot")
    plt.xlabel("Accuracy Ranges")
    plt.ylabel("Number of Games")
    plt.grid(True)
    plt.show()

def URL_opener(usernames, browser):

    print("Open your browser! This code will open new tabs in your browser!")
    print("It is essential that your browser is already opened!")
    print("To make sure that you aren't overwhelmed by the number of tabs,")
    print("the code will open the URLs, one category at a time (80%-85%, 85%-90%......).\n")
    
    input("Press any key to continue...")

    for user in usernames:
        directory = "Records/" + user + "/"
        files = os.listdir(directory)

        for file in files:
            txt_file = os.path.join(directory, file)
            with open(txt_file, "r") as file:
                urls = file.readlines()

            urls = [url.strip() for url in urls]

            print(f"\nOpening URLs from {txt_file} now...")
            input("Press any key to continue...")
            print("\n")

            for url in urls:
                print(url)
                webbrowser.get(f'"{browser}" %s').open(url)


def main():
    n = int(input("Enter the number of usernames (results will show a combined analysis): "))
    usernames = []
    for i in range(n):
        username = input(f"Enter username {i + 1}: ")
        usernames.append(username)
    
    print("\n")
    
    categorizer(usernames)
    if input("Do you want to see the statistics? (y/n): ").lower() == 'y':
        stats(usernames)
    if input("Do you want to open the URLs in your browser? (y/n): ").lower() == 'y' and input("This could potentially open a lot of tabs.\nYou can still open them manually from the exported files.\nAre you sure? (y/n): ").lower() == 'y':
        browser = input("Enter the path to your browser executable: ")
        print("\n")
        URL_opener(usernames, browser)
        print("All URLs opened!\n")


if __name__ == "__main__":
    main()