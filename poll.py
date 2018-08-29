class poll:
    def __init__(self, name):
        self.name = name
        self.selections = {}
        self.message_ids = []

    def add_message(self, chat_id, message_id):
        if (chat_id, message_id) not in self.message_ids:
            self.message_ids.append((chat_id, message_id))
        return self.message_ids

    def addselection(self, selection):
        self.selections[selection] = []

    def get_name(self):
        return self.name

    def get_message_ids(self):
        return self.message_ids

    def getselections(self):
        return self.selections

    def getresults(self):
        out = {}
        for sel in self.selections:
            out[sel] = len(self.selections[sel])
        return out

    def deleteselection(self, selection):
        selection.remove(selection)

    def vote(self, user, selection):
        print(user, selection)
        print(self.selections)
        for sel in self.selections.values():
            if user in sel:
                sel.remove(user)
                break
        self.selections[selection].append(user)

