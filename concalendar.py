import time, pickle
class calendar:
    def __init__(self):
        self.data = []
        self.noms = []
        self.active_con = None
        self.load()

    def accept_nom(self, con):
        self.load()
        for nom in self.noms:
            if nom[1] == con:
                self.add_con(nom[1])
                self.attend(nom[0], nom[1])
                self.noms.remove(nom)
        self.save()
        return

    def add_con(self, name, date = (2017, 1, 1, 0, 0, 0, 0, 0, 0)):
        self.data.append(convention(name, date))
        self.data = sorted(self.data, key=lambda con: con.date)
        self.save()
        return

    def attend(self, name, con):
        for i in self.data:
            if i.get_name() == con:
                i.add_attendee(name)
        self.save()
        return

    def clear(self):
        self.data = []
        self.noms = []
        self.save()

    def cons_by_user(self, name):
        out = []
        for con in self.data:
            if name in con.get_attendees():
                out.append(con.get_name())
        return out

    def date_change(self, name, newdate):
        for con in self.data:
            if con.get_name() == name:
                con.date.change(newdate)
                return
    def delete_con(self, con):
        for i in self.data:
            if i.get_name() == con:
                self.data.remove(i)
                break
        self.save()
        return

    def deselect(self):
        self.active_con = None
        return

    def display(self):
        outlist = []
        for con in self.data:
            out = ""
            out += time.asctime(con.date)[4:10] + ", " + time.asctime(con.date)[20:24] + "\n" + con.name + "\n"
            if con.get_location() != " ":
                out += con.get_location() + "\n"
            for attendee in con.attendees:
                try:
                    out += "- @" + attendee + "\n"
                except TypeError:
                    continue
            outlist.append(out)
        return outlist

    def get_active_con(self):
        return self.active_con

    def get_cons(self):
        out = []
        for con in self.data:
            out.append(con.get_name())
        return out

    def get_con(self, name):
        for con in self.data:
            if con.get_name() == name:
                return con

    def get_noms(self):
        self.load()
        return self.noms

    def load(self):
        (self.data, self.noms) = pickle.load(open("calendar_data.p", "rb"))
        return

    def nominate(self, name, con):
        self.load()
        self.noms.append((name, con))
        self.save()

    def reject_nom(self, con):
        self.load()
        for nom in self.noms:
            if nom[1] == con:
                self.noms.remove(nom)
        self.save()

    def save(self):
        pickle.dump((self.data, self.noms), open("calendar_data.p", "wb"))
        return

    def select_con(self, con):
        for i in self.data:
            if i.get_name() == con:
                self.active_con = i
                break
        return

    def update(self):
        self.data = sorted(self.data, key=lambda con: con.date)
        self.save()
        return

    def remove(self, name, con):
        for i in self.data:
            if i.get_name() == con:
                if name in i.get_attendees():
                    i.remove_attendee(name)
        self.save()
        return


class convention:
    def __init__(self, name, date):
        self.name = name
        self.date = date
        self.location = " "
        self.attendees = []
        return

    def add_attendee(self, name):
        if name not in self.attendees:
            self.attendees.append(name)
        return

    def change_name(self, newname):
        self.name = newname
        return

    def change_date(self, newdate):
        self.date = newdate

    def get_date(self):
        out = (time.asctime(self.date))[4:10] + " " + (time.asctime(self.date))[20:24]
        return out

    def get_name(self):
        return self.name

    def get_location(self):
        return self.location

    def remove_attendee(self, name):
        if name in self.attendees:
            self.attendees.remove(name)
        return

    def get_attendees(self):
        return self.attendees


    def set_location(self, loc):
        self.location = loc
        return