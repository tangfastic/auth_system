import auth_system

# Set up a test user and permission
auth_system.authenticator.add_user("joe", "joepassword")
auth_system.authoriser.add_permission("test program")
auth_system.authoriser.add_permission("change program")
auth_system.authoriser.permit_user("test program", "joe")

class Editor:
    def __init__(self,):
        self.username = None
        self.menu_map = {
            "login": self.login,
            "test": self.test,
            "change": self.change,
            "quit": self.quit
            }

    def login(self):
        logged_in = False
        while not logged_in:
            username = input("username: ")
            password = input("password: ")
            try:
                logged_in = auth_system.authenticator.login(username, password)
            except auth_system.InvalidUsername:
                print("Sorry, that username does not exist")
            except auth_system.InvalidPassword:
                print("Sorry, incorrect password")
            else:
                self.username = username

    def is_permitted(self, permission):
        try:
            auth_system.authoriser.check_permission(permission, self.username)
        except auth_system.NotLoggedInError as e:
            print("{} is not logged in".format(e.username))
            return False
        except auth_system.NotPermittedError as e:
            print("{} cannot {}".format(e.username, permission))
            return False
        else:
            return True

    def test(self):
        if self.is_permitted("test program"):
            print("Testing program now...")

    def change(self):
        if self.is_permitted("change program"):
            print("Changing program now...")

    def quit(self):
        raise SystemExit()

    def menu(self):
        try:
            answer = ""
            while True:
                print("""
Please enter a command:
\tlogin\tLogin
\ttest\tTest the program
\tchange\tChange the program
\tquit\tQuit
""")
                answer = input("enter a command: ").lower()
                try:
                    func = self.menu_map[answer]
                except KeyError:
                    print("{} is not a valid option".format(answer))
                else:
                    func()

        finally:
            print("Thank you for testing the auth_system module")

Editor().menu()
