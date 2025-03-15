from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import json
import os

# Replace with your actual BotFather token
TOKEN = '8129296827:AAHwjyWhyjlNvJB24xOXk2GyDF2uKZVr2Ow'

# Admin user IDs (replace with your Telegram user ID)
ADMIN_IDS = [7583523087]
ADMIN_IDS = [2059396078]# Replace with your actual Telegram user ID

# Options
GRADE_OPTIONS = ['9th', '10th', '11th', '12th']
SUBJECT_OPTIONS = ['English', 'Math', 'Biology', 'Chemistry', 'Physics']
CATEGORY_OPTIONS = ['Notes', 'Cheatsheets', 'Textbooks', 'Text', 'Videos']

# Persistent storage file
DB_FILE = 'resources_db.json'

# In-memory storage for resources (category -> grade -> subject -> file_id or text)
resources_db = {
    'notes': {},
    'cheatsheets': {},
    'textbooks': {},
    'text': {},
    'videos': {}
}

# Default resources (replace 'text' with actual file ID if needed)
DEFAULT_RESOURCES = {
    'notes': "Open Notes Resources:\n- MIT OpenCourseWare: https://ocw.mit.edu\n- Open Yale Courses: https://oyc.yale.edu",
    'cheatsheets': "Open Cheatsheets:\n- Cheatography: https://www.cheatography.com\n- Overleaf LaTeX: https://www.overleaf.com/learn/latex",
    'textbooks': "Open Textbooks:\n- OpenStax: https://openstax.org\n- BookSC: https://booksc.org",
    'text': 'No file or link provided yet.',
    'videos': "Open Video Resources:\n- Crash Course: https://www.youtube.com/user/crashcourse\n- Khan Academy: https://www.khanacademy.org"
}

# Load resources from JSON file
def load_resources():
    global resources_db
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            resources_db = json.load(f)
            print("Loaded resources from file:", resources_db)

# Save resources to JSON file
def save_resources():
    with open(DB_FILE, 'w') as f:
        json.dump(resources_db, f)
        print("Saved resources to file:", resources_db)

# Command to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Welcome to the Open Educational Resources (OER) Bot!\n"
        "Explore freely available educational content.\nAdmins can use /addresource to add materials."
    )
    await show_main_menu(update, context)

# Show the main menu
async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [['Notes', 'Cheatsheets'], ['Textbooks', 'Text'], ['Videos']]
    await update.message.reply_text(
        "Choose a category:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)
    )

# Show grade selection menu
async def show_grade_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str) -> None:
    context.user_data['category'] = category.lower()
    keyboard = [['9th', '10th'], ['11th', '12th'], ['Back']]
    await update.message.reply_text(
        f"Select a grade for {category}:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    )

# Show subject selection menu
async def show_subject_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, grade: str) -> None:
    context.user_data['grade'] = grade
    keyboard = [['English', 'Math'], ['Biology', 'Chemistry'], ['Physics'], ['Back']]
    await update.message.reply_text(
        "Select a subject:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    )

# Handle user input for browsing resources
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.strip() if update.message.text else None
    print(f"Received message: {text}, User data: {context.user_data}, Document: {update.message.document is not None}")
    
    if not text and not update.message.document:
        return
    
    # Handle admin form steps first
    if 'add_step' in context.user_data:
        await handle_add_resource_steps(update, context)
        return
    
    # Handle main menu options
    if text in CATEGORY_OPTIONS:
        await show_grade_menu(update, context, text)
        return
    
    # Handle grade selection
    category = context.user_data.get('category')
    if text == 'Back' and category and 'grade' not in context.user_data:
        await show_main_menu(update, context)
        context.user_data.clear()
        return
    elif text in GRADE_OPTIONS and category:
        await show_subject_menu(update, context, text)
        return
    
    # Handle subject selection
    grade = context.user_data.get('grade')
    if text == 'Back' and grade:
        await show_grade_menu(update, context, category)
        del context.user_data['grade']
        return
    elif text in SUBJECT_OPTIONS and grade and category:
        await provide_resources(update, context, category, grade, text)
        context.user_data.clear()
        return
    
    await update.message.reply_text("Please select a valid option.")

# Provide resources based on category, grade, and subject
async def provide_resources(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str, grade: str, subject: str) -> None:
    resource = resources_db[category].get(grade, {}).get(subject, DEFAULT_RESOURCES[category])
    print(f"Providing resource: {category} {grade} {subject} -> {resource}")
    
    if resource and not resource.startswith('http') and len(resource) > 10:  # Assume it's a file ID
        await update.message.reply_text(f"Sending {category} resource for {grade} {subject}...")
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=resource,
            caption=f"{category.capitalize()} resource for {grade} {subject}"
        )
    else:
        await update.message.reply_text(
            f"{category.capitalize()} for {grade} {subject}:\n{resource}"
        )
    await show_main_menu(update, context)

# Admin command to start adding resources
async def add_resource(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("You are not authorized to add resources.")
        return
    
    context.user_data['add_step'] = 'category'
    keyboard = [['Notes', 'Cheatsheets'], ['Textbooks', 'Text'], ['Videos'], ['Cancel']]
    await update.message.reply_text(
        "Select the category for the resource:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    )

# Handle the admin resource addition steps
async def handle_add_resource_steps(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.strip() if update.message.text else None
    step = context.user_data.get('add_step')
    print(f"Add step: {step}, Input: {text}, Document: {update.message.document is not None}")
    
    if text == 'Cancel':
        await update.message.reply_text("Resource addition cancelled.")
        context.user_data.clear()
        return
    
    if step == 'category' and text:
        if text in CATEGORY_OPTIONS:
            context.user_data['add_category'] = text.lower()
            context.user_data['add_step'] = 'grade'
            keyboard = [['9th', '10th'], ['11th', '12th'], ['Cancel']]
            await update.message.reply_text(
                "Select the grade:",
                reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            )
        else:
            await update.message.reply_text("Please select a valid category.")
    
    elif step == 'grade' and text:
        if text in GRADE_OPTIONS:
            context.user_data['add_grade'] = text
            context.user_data['add_step'] = 'subject'
            keyboard = [['English', 'Math'], ['Biology', 'Chemistry'], ['Physics'], ['Cancel']]
            await update.message.reply_text(
                "Select the subject:",
                reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            )
        else:
            await update.message.reply_text("Please select a valid grade.")
    
    elif step == 'subject' and text:
        if text in SUBJECT_OPTIONS:
            context.user_data['add_subject'] = text
            context.user_data['add_step'] = 'resource'
            await update.message.reply_text(
                "Please send the file or a link for this resource:",
                reply_markup=ReplyKeyboardMarkup([['Cancel']], one_time_keyboard=True)
            )
        else:
            await update.message.reply_text("Please select a valid subject.")
    
    elif step == 'resource':
        if update.message.document:
            context.user_data['add_resource'] = update.message.document.file_id
        elif text and not text.startswith('/'):  # Ignore commands
            context.user_data['add_resource'] = text
        else:
            await update.message.reply_text("Please send a file or a link.")
            return
        
        context.user_data['add_step'] = 'submit'
        keyboard = [['Submit'], ['Cancel']]
        resource_type = "File" if update.message.document else "Link"
        await update.message.reply_text(
            f"Confirm resource addition:\n"
            f"Category: {context.user_data['add_category']}\n"
            f"Grade: {context.user_data['add_grade']}\n"
            f"Subject: {context.user_data['add_subject']}\n"
            f"{resource_type} provided. Ready to submit?",
            reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        )
    
    elif step == 'submit' and text == 'Submit':
        category = context.user_data['add_category']
        grade = context.user_data['add_grade']
        subject = context.user_data['add_subject']
        resource = context.user_data['add_resource']
        
        if grade not in resources_db[category]:
            resources_db[category][grade] = {}
        resources_db[category][grade][subject] = resource
        save_resources()  # Save to JSON file
        await update.message.reply_text(f"Resource added for {category} {grade} {subject} successfully!")
        context.user_data.clear()

# List resources for debugging
async def list_resources(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("You are not authorized.")
        return
    response = "Added Resources:\n"
    for category, grades in resources_db.items():
        for grade, subjects in grades.items():
            for subject, resource in subjects.items():
                response += f"- {category} {grade} {subject}: {resource[:20]}...\n"
    await update.message.reply_text(response or "No resources added yet.")

# Error handler
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Error occurred: {context.error}")
    if update and update.message:
        await update.message.reply_text("An error occurred. Please try again.")

# Set up the application
def main() -> None:
    try:
        application = Application.builder().token(TOKEN).build()

        # Register handlers
        application.add_handler(CommandHandler('start', start))
        application.add_handler(CommandHandler('addresource', add_resource))
        application.add_handler(CommandHandler('listresources', list_resources))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND | filters.Document.ALL, handle_message))
        application.add_error_handler(error_handler)

        # Load resources from file
        load_resources()

        # Start the bot
        print("OER Bot is running...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        print(f"Failed to start bot: {e}")

if __name__ == '__main__':
    main()
