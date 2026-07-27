from knitting_project import KnittingProject
from knitting_commands import KnittingCommands
from voice_listener import Listener
from projects import load, save, delete
from speaker import Speaker


class App:
    def __init__(self):
        print("App starting...", flush=True)
        self.projects, current_project_name = load()
        print("Projects loaded...", flush=True)
        self.current_project = self.projects.get(current_project_name)
        self.handler = KnittingCommands(
            self.current_project,
            self.on_create_project,
            self.on_save,
            self.on_delete_project,
        )
        self.speaker = Speaker()
        self.listener = Listener(self.handler, self.speaker)

    # TO DO seperate this method into create_project and on_create_project and move one
    def on_create_project(self, name):
        new_project = KnittingProject(name)
        self.projects[name] = new_project
        self.current_project = new_project
        self.handler.current_project = new_project
        save(self.projects, name)

    def on_delete_project(self, name):
        result = delete(self.projects, name)
        # If project has been deleted and that project is current project
        if result and self.current_project == name:
            self.current_project = None
            self.handler.project = None
        if self.current_project:
            save(self.projects, self.current_project.name)
        else:
            save(self.projects, None)
        return result

    def on_save(self):
        save(self.projects, self.current_project.name)

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
