import os
import requests

usernames = ["new_account", "old_account", "another_account", "account4"]  # Replace with your usernames

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

def main():
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
                print(f"Saving review URLs to {user + '/' + str(threshold_lower) + '.txt'}...\n")
                save_urls_to_txt(final_urls, "Records/" + user + '/' + str(threshold_lower) + "-" + str(threshold_upper) + '.txt')
            threshold_lower = threshold_lower - 5.0
        print(f"Finished processing for {user}.\n\n")
    print(f"Total games analyzed: {total_analyzed}\n")

if __name__ == "__main__":
    main()