# Chess.com Analyzer

> _Note: This tool is unofficial and not affiliated with Chess.com._

**A simple tool to analyze your Chess.com account** — works using all games you have **already** game-reviewed.

There are 3 Python scripts included:
- **Categorizer**
- **Statistics**
- **Auto URL Opener**

The only thing you need to do is add your username to the code.

## 🖥️ Executable file included
**Additionally, you can go to releases to get the newest executable file**

---

## 📂 Categorizer

- Browses through every game you have ever played.
- Filters out games that **haven't been game-reviewed** yet.
- Categorizes reviewed games into classes with a **5% width** (e.g., 80–85%, 85–90% accuracy).
- Exports each category into a separate `.txt` file containing URLs of the games.
- Supports **multiple usernames**, allowing you to check your old and new accounts at once.

---

## 📊 Statistics

> **Requires Categorizer to be run at least once.**

- Gathers all categorized games.
- Calculates:
  - Total games analyzed
  - Mean accuracy
  - Median accuracy
  - Mode accuracy (**can be multiple modes**)
  - Frequency list of accuracies (divided into 5% ranges from 0% to 100%)
- Displays a **graph** showing the distribution of accuracies.

---

## 🌐 Auto URL Opener

> **Requires Categorizer to be run at least once.**

- Automatically opens all links stored in the categorized files.
- Useful for finding specific moments like **Brilliant moves** without manually opening each game.
- You can delete any `.txt` files of unwanted accuracy ranges — they’ll regenerate when you rerun Categorizer.

---

## 🚀 How to Use

1. Run **Categorizer** first to sort your games.
2. (Optional) Run **Statistics** to view detailed metrics and graphs.
3. (Optional) Run **Auto URL Opener** to quickly browse through your categorized games.

---

## 🛠 Technologies Used

- Python 3
- `requests`
- `matplotlib`
- Standard libraries: `os`, `webbrowser`

---

## 📝 Notes

- Make sure your games are **already reviewed** on Chess.com before using the scripts.
- Deleting categorized `.txt` files is fine — they’ll regenerate after rerunning Categorizer.
- **Mode** in Statistics can have multiple values if more than one accuracy range has the highest frequency.
- This project is made for **personal use** but feel free to adapt it however you like!

---

## 🐞 Known Issues

- **Occasional incorrect accuracy values:**  
  Sometimes, Chess.com itself stores wrong accuracy values through their API.
  This is very rare, but when it happens, there is nothing this tool can do to fix it. Hence, this error will remain until chess.com itself fixes it.

  Example from a real game:
  ```json
  "accuracies": {
      "white": 27.1478279059976,
      "black": 24.4236226583375
  }
  ```
  However, according to manual Game Review:
  - **White:** 68.8%
  - **Black:** 64.2%

- **Suggested Handling Method:**  
  Since all URLs are categorized into separate files based on accuracy ranges, it is recommended that:
  - You manually open the URLs from files containing wrong data.
  - **Relocate** those games into their appropriate accuracy files.
  - Remember, Statistics are calculated based on the **count of URLs** in each file.

  Alternatively:
  - You can **delete** files with very low accuracies if you notice errors.
  - However, deleting is **mathematically less accurate** than relocating.

- **Practical Note:**  
  These errors are extremely rare.  
  Even if you **ignore** them entirely, the impact on the overall statistics will be **negligible** compared to the large number of correctly categorized games.

---

- **Drifted Accuracies**
  Drifted Accuracies are inaccuracies that are very close (within ±5%) to the actual accuracy when manually reviewed. This discrepancy is likely caused by recalibration or changes to Chess.com’s analysis system.
  
  The major problem with Drifted Accuracies is that there is no way to distinguish them from correct values. They are mixed in with the correctly categorized games, and there is no method to identify or fix them.
  
  Unlike Incorrect Accuracies, which can be found in files with abnormally low values (lower than 30%), Drifted Accuracies appear normal and cannot be detected without manually checking every single game.

  Since they cannot be identified or corrected automatically, Drifted Accuracies will remain in the dataset. Their impact on overall statistics is minimal, as they only slightly differ from the actual accuracy (within a ±5% margin), but the fact that they cannot be handled or excluded means they are a known issue and will also remain until chess.com itself fixes it.

---

## 📄 License

This project is open-source and free to use under the [MIT License](LICENSE).
