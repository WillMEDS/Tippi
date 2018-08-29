import poll
import pickle

class chatcontainer:
    def __init__(self):
        self.groups = []
        self.load()

    def load(self):
        self.groups = pickle.load(open("chatdata.p", "rb"))

    def add_admin(self, user_id, group):
        for i in self.get_chats():
            if i.get_name() == group:
                i.admin(user_id)
                self.save()
                return
        raise "Group not found"

    def add_chat(self, name, chat_id = 0):
        self.groups.append(chat(name, chat_id))
        self.save()
        return

    def add_poll(self, name, group):
        for i in self.groups:
            if i.get_name() == group:
                i.add_poll(name)
                self.save()
                return
        raise "Group not found"

    def delete_poll(self, group):
        chat  = self.get_chat(group)
        chat.delete_poll()
        self.save()
        return

    def get_all_polls(self):
        out = []
        for i in self.groups:
            poll = i.get_poll()
            if poll != None:
                out.append(poll)
        return out

    def get_chats(self):
        return self.groups

    def get_chat(self, group):
        for i in self.groups:
            if i.get_name() == group:
                return i
        return None

    def get_poll(self, group):
        chat = self.get_chat(group)
        return chat.get_poll()

    def save(self):
        pickle.dump(self.groups, open("chatdata.p", "wb"))
        return

class chat:
    def __init__(self, name, chat_id):
        self.name = name
        self.chat_id = chat_id
        self.admins = []
        self.poll = None
		self.event = None
		
    def admin(self, user_id):
        self.admins.append(user_id)
        return 0

	def event_add(self, name)
		self.event = Name
    def delete_poll(self):
        self.poll = None

    def get_admins(self):
        return self.admins

    def get_id(self):
        return self.chat_id

    def get_name(self):
        return self.name

    def get_poll(self):
        return self.poll

    def add_poll(self, name):
        self.poll = poll.poll(name)

    def poll_addmessageid(self, message_id):
        self.poll.add_message(message_id)
        return

chatcontainer = chatcontainer()
#groups = {}
#groups["msanthro"] = chat("msanthro", -1001083134008)
#groups["starkville"] = chat("starkville")
#groups["msanthro"].admin(263490798) #MEDS user id
#groups["starkville"].admin(263490798) #MEDS user id