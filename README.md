
# Open Educational Resources (OER) Bot

A Telegram bot built with Python and the `python-telegram-bot` library to provide open educational resources (OER) such as notes, cheatsheets, textbooks, text, and videos. Users can browse resources by category, grade, and subject, while admins can add new resources (files or links) to the database. The bot uses a JSON file for persistent storage.

## Features

- **Browse Resources**: Users can explore educational content categorized by type (e.g., Notes, Textbooks), grade (9th–12th), and subject (English, Math, Biology, Chemistry, Physics).
- **Admin Functionality**: Authorized admins can add new resources (files or links) via the `/addresource` command.
- **Persistent Storage**: Resources are stored in a JSON file (`resources_db.json`) for persistence across restarts.
- **Default Resources**: Predefined open educational links are provided when no custom resources are available.
- **Interactive Menus**: Custom keyboards guide users through the selection process.

## Prerequisites

- **Python 3.7+**
- **Telegram Bot Token**: Obtain a token from [BotFather](https://t.me/BotFather) on Telegram.
- **Dependencies**: Install required Python packages (see [Installation](#installation)).

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/oer-bot.git
   cd oer-bot
   ```

2. **Install Dependencies**:
   ```bash
   pip install python-telegram-bot
   ```

3. **Set Up Configuration**:
   - Open the `oer_bot.py` file.
   - Replace the `TOKEN` placeholder with your BotFather token:
     ```python
     TOKEN = 'your-bot-token-here'
     ```
   - Replace the `ADMIN_IDS` placeholder with your Telegram user ID:
     ```python
     ADMIN_IDS = [your_telegram_user_id]
     ```
     To find your Telegram user ID, message `@userinfobot` on Telegram.

4. **Run the Bot**:
   ```bash
   python oer_bot.py
   ```

## Usage

1. **Start the Bot**:
   - Send `/start` to the bot on Telegram to see the welcome message and main menu.

2. **Browse Resources**:
   - Select a category (e.g., Notes, Textbooks).
   - Choose a grade (9th, 10th, 11th, 12th).
   - Pick a subject (English, Math, Biology, Chemistry, Physics).
   - The bot will send the resource (file or link) or default open resources if none are added.

3. **Admin Commands**:
   - `/addresource`: Start the process to add a new resource (admin only).
     - Follow the prompts to select category, grade, subject, and upload a file or send a link.
   - `/listresources`: View all added resources (admin only).

4. **Navigation**:
   - Use the "Back" button to return to the previous menu.
   - Use "Cancel" during resource addition to abort the process.

## File Structure

- `oer_bot.py`: Main bot script containing all logic.
- `resources_db.json`: Persistent storage file for resources (created automatically on first save).

## Example Resources Database

The bot stores resources in the following structure:
```json
{
  "notes": {
    "9th": {
      "Math": "file_id_or_link"
    }
  },
  "cheatsheets": {},
  "textbooks": {},
  "text": {},
  "videos": {}
}
```
- Default resources are provided as links to open educational platforms (e.g., OpenStax, Khan Academy).

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

## Troubleshooting

- **Bot Not Responding**: Ensure the token is correct and the bot is running.
- **Permission Errors**: Verify your Telegram user ID is in `ADMIN_IDS` for admin commands.
- **File Not Found**: The `resources_db.json` file is created automatically when a resource is added; no need to create it manually.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot).
- Inspired by the need for accessible open educational resources.


### Notes:
- Replace `yourusername` in the clone URL with your actual GitHub username.
- Add a `LICENSE` file to your repository if you want to include licensing (e.g., MIT License).
- You might want to add screenshots or a demo video in the README to showcase the bot’s functionality.

