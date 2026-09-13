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

    def save(self):
        #if self.current_project is None:
            #self.current_project = name
        file_path = "projects.json"
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
            self.current_project = None

        self.save()
        return True

    def new_project(self, name):
        new_project = KnittingProject(name)
        self.current_project = name
        self.projects[name] = new_project
        self.save()

    def get_current_project(self):
        if self.current_project is None:
            return None
        else:
            return self.projects[self.current_project]

    def switch(self, name):
        if name not in self.projects:
            return False
        else:
            self.current_project = name
            self.save()
            return True

    

    # returns all project names in one string
    def all_project_names(self):
        names = list(self.projects.keys())
        names_string = " ".join(names)
        return names_string

    def project_grammer_string(self):
        grammer_string = '["'
        names = list(self.projects.keys())
        names_string = '", "'.join(names)
        grammer_string += names_string
        grammer_string += '", "[unk]"]'
        return grammer_string