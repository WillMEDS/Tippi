from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import config, chats, concalendar
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
import logging
def main():
    def admin(bot, update, group):
        for i in chats.chatcontainer.get_chats():
            print(group, i.get_name())
            if i.get_name() == group:
                print(update.message.from_user.id, i.get_admins())
                if update.message.from_user.id in i.get_admins():
                    return True
        return False

    def build_menu(buttons, n_cols, header_buttons = None, footer_buttons = None):
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, header_buttons)
        if footer_buttons:
            menu.append(footer_buttons)

        return menu

    def callback(bot, update):
        query = update.callback_query
        print(query.data)

        if query.data == "view_concalendar":
            out = "---ConCalendar---\n\n"
            cal = (calendar.display())
            for con in cal:
                query.message.reply_text(text=con)
            return

        if query.data == "my_cons":
            out = "Your cons:\n"
            for con in calendar.cons_by_user(query.from_user.username):
                out += "\n %s" % con
            buttons = build_menu([InlineKeyboardButton("Add", callback_data="add_con"),
                                  InlineKeyboardButton("Remove", callback_data="remove_con")], 2)
            reply_markup = InlineKeyboardMarkup(buttons)
            query.message.reply_text(text=out, reply_markup=reply_markup)
            return

        if query.data == "add_con":
            button_list = []
            for con in calendar.get_cons():
                button_list.append(InlineKeyboardButton(con, callback_data= "addcon" + con))
            buttons = build_menu(button_list, 1, footer_buttons=[InlineKeyboardButton("Add a convention not listed", callback_data= "nom_con")])
            print(buttons)
            reply_markup = InlineKeyboardMarkup(buttons)
            query.message.reply_text(text="Select the con that you will be attending.", reply_markup=reply_markup)
            return

        if query.data == "remove_con":
            button_list = []
            for con in calendar.cons_by_user(query.from_user.username):
                button_list.append(InlineKeyboardButton(con, callback_data="rmcon" + con))
            buttons = build_menu(button_list, 1)
            reply_markup = InlineKeyboardMarkup(buttons)
            query.message.reply_text(text="Select the con that you will be not be attending.", reply_markup=reply_markup)
            return

        if query.data[0:6] == "addcon":
            calendar.attend(query.from_user.username, query.data[6:])
            bot.editMessageText(text="You are attending %s!" % query.data[6:], chat_id=query.message.chat_id, message_id=query.message.message_id)
            return

        if query.data[0:5] == "rmcon":
            calendar.remove(query.from_user.username, query.data[5:])
            bot.editMessageText(text="You are no longer attending %s!" % query.data[5:], chat_id=query.message.chat_id, message_id=query.message.message_id)
            return

        if query.data == "nom_con":
            updater.dispatcher.add_handler(MessageHandler(Filters.text, nom_con))
            bot.editMessageText(text="Please send the name of the convention now.", chat_id=query.message.chat_id, message_id=query.message.message_id)
            return

        if query.data[0:10] == "accept_nom":
            if admin(bot, query, "msanthro"):
                con = query.data[10:]
                calendar.accept_nom(con)
                bot.editMessageText(text="%s has been accepted." % con, chat_id=query.message.chat_id, message_id=query.message.message_id)
            return

        if query.data[0:10] == "reject_nom":
            if admin(bot, query, "msanthro"):
                con = query.data[10:]
                calendar.reject_nom(con)
                bot.editMessageText(text="%s has been rejected." % con, chat_id=query.message.chat_id, message_id=query.message.message_id)
            return

        if query.data == "manage":
            if admin(bot, query, "msanthro"):
                button_list = []
                for con in calendar.get_cons():
                    button_list.append(InlineKeyboardButton(con, callback_data="modcon" + con))
                buttons = build_menu(button_list, 1)
                reply_markup = InlineKeyboardMarkup(buttons)
                query.message.reply_text(text="Select the item that you would like to modify", reply_markup=reply_markup)
            return

        if query.data[0:6] == "modcon":
            if admin(bot, query, "msanthro"):
                con = calendar.get_con(query.data[6:])
                buttons = build_menu([InlineKeyboardButton("Change name", callback_data= "nmchng" + con.get_name()),
                                      InlineKeyboardButton("Change date", callback_data= "datechng" + con.get_name()),
                                      InlineKeyboardButton("Change Location", callback_data="locchng" + con.get_name()),
                                      InlineKeyboardButton("Delete", callback_data= "delete" + con.get_name())], 2)
                reply_markup = InlineKeyboardMarkup(buttons)
                bot.editMessageText(text="%s\n%s\n%s" % (con.get_name(), con.get_date(), con.get_location()), chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=reply_markup)
            return

        if query.data[0:6] == "nmchng":
            if admin(bot, query, "msanthro"):
                calendar.select_con(query.data[6:])
                active_con = calendar.get_active_con()
                updater.dispatcher.add_handler(MessageHandler(Filters.text, nmchng_con))
                bot.editMessageText(text="Enter a new name for %s" % active_con.get_name(), chat_id=query.message.chat_id,message_id=query.message.message_id)
            return

        if query.data[0:4] == "poll":
            poll_name = query.data[4:]
            if private(bot, query, warn=False):
                chat_id = query.message.chat_id
                for chat in chats.chatcontainer.get_chats():
                    print(chat_id, chat.get_id())
                    if chat_id == chat.get_id():
                        print("match")
                        announce_poll(bot, query, [chat.get_name(), chat.get_name()])
                        return




        if query.data[0:8] == "datechng":
            if admin(bot, query, "msanthro"):
                calendar.select_con(query.data[8:])
                active_con = calendar.get_active_con()
                updater.dispatcher.add_handler(MessageHandler(Filters.text, datechng_con))
                bot.editMessageText(text="Enter a new date for %s (format YYYYMMDD)" % active_con.get_name(), chat_id=query.message.chat_id, message_id=query.message.message_id)
            return

        if query.data[0:7] == "locchng":
            if admin(bot, query, "msanthro"):
                calendar.select_con(query.data[7:])
                active_con = calendar.get_active_con()
                updater.dispatcher.add_handler(MessageHandler(Filters.text, locchng_con))
                bot.editMessageText(text="Enter a new location for %s" % active_con.get_name(),
                                    chat_id=query.message.chat_id, message_id=query.message.message_id)
        if query.data[0:6] == "delete":
            if admin(bot, query, "msanthro"):
                calendar.delete_con(query.data[6:])
                bot.editMessageText(text="%s has been deleted" % query.data[6:],
                                    chat_id=query.message.chat_id, message_id=query.message.message_id)

        if query.data == "announce":
            print("announce triggered")
            if admin(bot, query, "msanthro"):
                print("authenticated")
                bot.sendMessage(chat_id= -1001083134008, text=calendar.display())

        if query.data[0:4] == "vote":
            split_callback = query.data.split()
            del split_callback[0]
            group = split_callback[0]
            del split_callback[0]
            selection = " ".join(split_callback)
            poll = chats.chatcontainer.get_poll(group)
            poll.vote(query.from_user.first_name, selection)
            chats.chatcontainer.save()
            update_poll(bot, query, group)

    def clear_poll(bot, update, args):
        try:
            group = args[0]
        except IndexError:
            update.message.reply_text("Invalid syntax\n/clearpoll group")
        else:
            try:
                chats.chatcontainer.delete_poll(group)
            except AttributeError:
                update.message.reply_text("Group not found")
            else:
                update.message.reply_text("Poll deleted")

    def conventioncalendar(bot, update):
        if private(bot, update):
            #menu = build_menu(["View", "My Cons"], 1)
            #update.message.reply_text(menu)
            if admin(bot, update, "msanthro"):
                admin_buttons = [InlineKeyboardButton("Manage", callback_data="manage"),
                                  InlineKeyboardButton("Announce", callback_data="announce")]
            else:
                admin_buttons = None
            buttons = build_menu([InlineKeyboardButton("View", callback_data="view_concalendar"),
                                  InlineKeyboardButton("My Cons", callback_data="my_cons")], 2, footer_buttons=admin_buttons)

            reply_markup = InlineKeyboardMarkup(buttons)

            update.message.reply_text('Please choose:', reply_markup=reply_markup)

    def nmchng_con(bot, update):
        updater.dispatcher.remove_handler(updater.dispatcher.handlers[0][-1])
        active_con = calendar.get_active_con()
        active_con.change_name(update.message.text)
        update.message.reply_text(text="Name has been changed to  %s" % active_con.get_name())
        calendar.deselect()

    def datechng_con(bot, update):
        active_con = calendar.get_active_con()
        newdate = update.message.text
        updater.dispatcher.remove_handler(updater.dispatcher.handlers[0][-1])
        active_con.change_date((int(newdate[0:4]), int(newdate[4:6]), int(newdate[6:8]), 0, 0, 0, 0, 0, 0))
        update.message.reply_text(text="Date has been changed to  %s" % active_con.get_date())
        calendar.deselect()
        calendar.update()

    def locchng_con(bot, update):
        active_con = calendar.get_active_con()
        loc = update.message.text
        updater.dispatcher.remove_handler(updater.dispatcher.handlers[0][-1])
        active_con.set_location(loc)
        update.message.reply_text(text="Location has been changed to  %s" % active_con.get_location())
        calendar.deselect()
        calendar.save()

    def nom_con(bot, update,):
        calendar.nominate(update.message.from_user.username, update.message.text)
        updater.dispatcher.remove_handler(updater.dispatcher.handlers[0][-1])
        update.message.reply_text("Excellent! I'll notify you when the concalendar is updated")
        buttons = build_menu([InlineKeyboardButton("Accept", callback_data="accept_nom" + update.message.text),
                              InlineKeyboardButton("Reject", callback_data="reject_nom" + update.message.text)], 2)
        reply_markup = InlineKeyboardMarkup(buttons)
        bot.sendMessage(chat_id=263490798, text="%s has nominated %s for the concalendar." % (update.message.from_user.username, update.message.text), reply_markup=reply_markup)


    def private(bot, update, warn=True):
        if update.message.chat.type != "private":
            if warn:
                out = "You should only use that command in a private chat."
                update.message.reply_text(out)
            return False
        return True

    def start(bot, update):
        if private(bot, update):
            out = "Hello, I'm Tippi, the helpful fox. What can I do for you?\n\n" \
                "/concalendar - A directory for people attending cons.\n" \
                "/poll - Vote in active polls"
            update.message.reply_text(out)

    def hello(bot, update):
        update.message.reply_text('Hello {}'.format(update.message.from_user.first_name))

    def msanthro(bot, update, args):
        chat_id = -1001083134008
        delimeter = " "
        out = (delimeter.join(args))
        bot.sendMessage(chat_id=chat_id, text=out)
        return

    def newpoll(bot, update, args):
        try:
            group = args[0]
        except IndexError:
            update.message.reply_text("Invalid syntax:\n /newpoll group [name]")
        else:
            del args[0]
            if admin(bot, update, group):
                name =" ".join(args)
                for i in chats.chatcontainer.get_chats():
                    if i.get_name() == group:
                        chats.chatcontainer.add_poll(name, group)
                        out = "I've created a new poll called " + name
                        update.message.reply_text(out)
                        return
                out = "Failed"
                update.message.reply_text(out)
        return

    def poll(bot, update):
        out = "Here are the current polls:"
        button_list = []
        for i in chats.chatcontainer.get_chats():
            poll = i.get_poll()
            if poll != None:
                button_list.append(InlineKeyboardButton(poll.get_name(), callback_data= "poll" + poll.get_name()))
        if len(button_list) == 0:
            out = "There are no polls currently.\n"
        buttons = build_menu(button_list, 1)
        print(buttons)
        #reply_markup = InlineKeyboardMarkup(buttons)
        #update.message.reply_text(text=out, reply_markup=reply_markup)
        if admin(bot, update, "msanthro"):
            out += "\n\n/newpoll group [name]" \
                    "\n/addselection group" \
                    "\n/announcepoll group" \
                    "\n/clearpoll group"
        reply_markup = InlineKeyboardMarkup(buttons)
        update.message.reply_text(text=out, reply_markup=reply_markup)
		
	def rsvp(bot, update, args):
		group = args.pop(0)
		name = " ".join(args)
		if admin(bot, update, group):
		

    def select_poll(bot,update):
        if admin(bot, update, group):
            reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
            bot.sendMessage(chat_id=update.message.chat_id, text="Please select a poll", reply_markup=reply_markup)

    def addselection(bot, update, args):
        group = args.pop(0)
        selection = " ".join(args)
        if admin(bot, update, group):
            poll = chats.chatcontainer.get_poll(group)
            poll.addselection(selection)
            chats.chatcontainer.save()
            update_poll(bot, update, group)
            update.message.reply_text("%s has been added to %s" % (selection, poll.get_name()))
        return

    def vote(bot, update, args):
        if private(bot, update):
            if len(args) == 0:
                custom_keyboard = []
                for sel in active_poll.getselections():
                    custom_keyboard.append(["/vote " + sel])
                reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
                bot.sendMessage(chat_id= update.message.chat_id, text = "Please vote now.", reply_markup = reply_markup)
            else:
                reply_markup = telegram.ReplyKeyboardHide()
                selection = " ".join(args)
                active_poll.vote(update.message.from_user.first_name, selection)
                bot.send_message(chat_id=update.message.chat_id, text="Your vote has been recieved!", reply_markup=reply_markup)
        return

    def get_results(bot, update):
        out = "Here are the results from the current poll:\n" + active_poll.get_name() + " \n\n "
        for key,value in active_poll.getresults().items():
            out = out + key + ": " + str(value) + "\n"
        update.message.reply_text(out)
        return

    def announce_poll(bot, update, args):
        button_list = []
        group = args[0]
        sendgroup = args[1]
        print(group, sendgroup)
        poll = chats.chatcontainer.get_poll(group)
        print(group)
        msgchat = chats.chatcontainer.get_chat(sendgroup)
        print(msgchat)
        chat_id = msgchat.get_id()
        for selection in poll.getselections().keys():
            button_list.append(InlineKeyboardButton(selection, callback_data= "vote" + group + selection))
        buttons = build_menu(button_list, 1)
        reply_markup = InlineKeyboardMarkup(buttons)

        newmessage = bot.send_message(chat_id=chat_id, text="New poll loading...")
        print(newmessage)
        message_id = newmessage.message_id
        poll.add_message(chat_id, message_id)
        update_poll(bot, update, group)
        chats.chatcontainer.save()
        return

    def update_poll(bot, update, group):
        button_list = []
        poll = chats.chatcontainer.get_poll(group)
        out = poll.get_name() + "\n\n"
        for key,value in poll.getresults().items():
            print(key, value)
            out += key + ": " + str(value) +"\n"

        for selection in poll.getselections().keys():
            button_list.append(InlineKeyboardButton(selection, callback_data= "vote " + group + " " + selection))
        buttons = build_menu(button_list, 1)
        reply_markup = InlineKeyboardMarkup(buttons)
        print(poll.get_message_ids())
        for chat_id, message_id in poll.get_message_ids():
            print(chat_id, message_id)
            bot.editMessageText(text=out, chat_id=chat_id, message_id=message_id, reply_markup=reply_markup)

    def wom(bot, update):
        update.message.reply_text("WOM")

    def picturepoll(bot, update):
        print(update.message.chat_id)
        if update.message.chat_id == 263490798:
            print("yes")
        return

##initializing the chat objects

    admins = [263490798]

    calendar = concalendar.calendar()
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')





    updater = Updater('223383394:AAGsgqwgjrGr3SLksGpKWTR4qhQTCnz6wi8')

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.dispatcher.add_handler(CommandHandler('msanthro', msanthro, pass_args=True))
	updater.dispatcher.add_handler(CommandHandler('rsvp', rsvp, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('poll', poll))
    updater.dispatcher.add_handler(CommandHandler('newpoll', newpoll, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('addselection', addselection, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('vote', vote, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('results', get_results))
    updater.dispatcher.add_handler(CommandHandler('announcepoll', announce_poll, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('clearpoll', clear_poll, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('concalendar', conventioncalendar))
    updater.dispatcher.add_handler(MessageHandler(Filters.mow, wom))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback))
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, picturepoll))




    updater.start_polling()
    updater.idle()
    return

if __name__ == "__main__":
    main()