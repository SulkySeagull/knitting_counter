from knitting_project import KnittingProject
from knitting_commands import KnittingCommands
from voice_listener import Listener
from projects import Projects
from speaker import Speaker

class App:
    def __init__(self):
        print("App starting...", flush=True)
        self.knitting_projects = Projects.load()
        print("Projects loaded...", flush=True)
        self.handler = KnittingCommands(self.knitting_projects)
        self.speaker = Speaker()
        print("Speaker loaded...", flush=True)
        self.listener = Listener(self.handler, self.speaker)

    def run(self):
        print("Starting listener", flush=True)
        self.listener.start()


if __name__ == "__main__":
    try:
        app = App()
        app.run()
    except Exception as e:
        import traceback

        traceback.print_exc()
        input("Press enter to exit")
