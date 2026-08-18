import json
from knitting_project import KnittingProject

class Projects:

    def __init__(self):
        self.projects, self.current_project = self.load()

    def load(self):
        try:
            with open("projects.json", "r") as f:
                data = json.load(f)
                projects = {}
                for name, project in data["projects"].items():
                    projects[name] = KnittingProject.convert_to_python(project)
                return projects, data["current project"]
        except FileNotFoundError:
            return {}, None

    def save(self, file_path="projects.json"):
        projects_dict = {}
        for name, project in self.projects.items():
            projects_dict[name] = project.convert_to_json()

        data = {"current project": self.current_project, "projects": projects_dict}
        with open(file_path, "w") as f:
            json.dump(data, f)


    def delete(self, name):
        if name not in self.projects:
            return False

        del self.projects[name]

        if self.current_project == name:
            self.current = None

        self.save(self.projects, self.current_project)
        return True

    def create_new_project(self, name):
        new_project = KnittingProject(name)
        self.projects[name] = new_project
        self.current_project = new_project
        self.save(self.projects, name)

    def get_current_project(self):
        if self.current_project is None:
            return None
        else:
            return self.projects[self.current_project]

