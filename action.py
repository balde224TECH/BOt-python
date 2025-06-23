import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Listes d'actions et vérités
actions_easy = ["Fais 5 pompes.", "Danse sans musique pendant 10 secondes.", "Imite un chat."]
actions_medium = ["Chante une chanson pendant 30 secondes.", "Appelle quelqu'un et dis-lui que tu l'aimes.", "Fais un selfie avec une pose drôle."]
actions_hard = ["Mange une cuillère de moutarde.", "Essaie de jongler avec trois objets.", "Récite l'alphabet à l'envers."]
truths_easy = ["Quel est ton plat préféré ?", "As-tu un surnom ?", "Quel est ton animal préféré ?"]
truths_medium = ["Quel est ton plus grand rêve ?", "As-tu déjà menti pour te tirer d'une situation ?", "As-tu déjà triché à un examen ?"]
truths_hard = ["Quel est ton plus gros secret ?", "As-tu déjà trahi un ami proche ?", "Quelle est la pire bêtise que tu as faite ?"]

# Variables globales pour stocker les joueurs et leurs scores
players_scores = {}

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Action Facile", "Action Moyenne", "Action Difficile"], 
                ["Vérité Facile", "Vérité Moyenne", "Vérité Difficile"], 
                ["Ajouter une action", "Ajouter une vérité"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Bienvenue au jeu Action ou Vérité ! Choisissez une option :",
        reply_markup=reply_markup
    )

# Gestion des actions
async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.lower()
    username = update.message.from_user.username or "Invité"

    if user_input.startswith("action"):
        level = user_input.split()[1]
        if level == "facile":
            response = random.choice(actions_easy)
        elif level == "moyenne":
            response = random.choice(actions_medium)
        elif level == "difficile":
            response = random.choice(actions_hard)
        else:
            response = "Niveau non reconnu."
        await update.message.reply_text(f"Action ({level.capitalize()}) : {response}")
        players_scores[username] = players_scores.get(username, 0) + 1

    elif user_input.startswith("vérité"):
        level = user_input.split()[1]
        if level == "facile":
            response = random.choice(truths_easy)
        elif level == "moyenne":
            response = random.choice(truths_medium)
        elif level == "difficile":
            response = random.choice(truths_hard)
        else:
            response = "Niveau non reconnu."
        await update.message.reply_text(f"Vérité ({level.capitalize()}) : {response}")
        players_scores[username] = players_scores.get(username, 0) + 1

    elif user_input == "ajouter une action":
        await update.message.reply_text("Tapez l'action à ajouter :")
        context.user_data["adding_action"] = True

    elif user_input == "ajouter une vérité":
        await update.message.reply_text("Tapez la vérité à ajouter :")
        context.user_data["adding_truth"] = True

    elif "adding_action" in context.user_data:
        actions_easy.append(user_input)
        context.user_data.pop("adding_action")
        await update.message.reply_text("Action ajoutée avec succès !")

    elif "adding_truth" in context.user_data:
        truths_easy.append(user_input)
        context.user_data.pop("adding_truth")
        await update.message.reply_text("Vérité ajoutée avec succès !")

    else:
        await update.message.reply_text("Option non reconnue. Utilisez le menu.")

# Commande /scores
async def scores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not players_scores:
        await update.message.reply_text("Aucun joueur n'a encore de score.")
    else:
        scores_list = "\n".join([f"{player} : {score} points" for player, score in players_scores.items()])
        await update.message.reply_text(f"Scores actuels :\n{scores_list}")

# Fonction principale
def main():
    """Configurer le bot Telegram."""
    TELEGRAM_BOT_TOKEN = "7738217538:AAHYGV5jXPv5L37QmHsJ7PbnBz8UhXYof2k"
    
    # Créer l'application
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Ajouter les gestionnaires
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("scores", scores))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

    # Lancer le bot
    print("Bot en cours d'exécution...")
    app.run_polling()

if __name__ == "__main__":
    main()
