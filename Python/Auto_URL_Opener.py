import os
import webbrowser

usernames = ["new_account", "old_account", "another_account", "account4"]  # Replace with your usernames

for user in usernames:
    directory = "Records/" + user + "/"
    files = os.listdir(directory)

    for file in files:
        txt_file = os.path.join(directory, file)
        with open(txt_file, "r") as file:
            urls = file.readlines()

        urls = [url.strip() for url in urls]

        browser_path = r"C:\link\to\browser.exe"  # Replace with the path to your browser executable

        for url in urls:
            print(url)
            webbrowser.get(f'"{browser_path}" %s').open(url)

        print("All URLs are opened in your browser!")
        input("Press any key to continue...")

# MAKE SURE THAT YOUR BROWSER IS ALREADY OPENED
# THIS WILL ONLY OPEN TABS
# IF NOT ALREADY OPENED, IT WILL BEHAVE ERRATICALLY
