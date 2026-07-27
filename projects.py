import json
from knitting_project import KnittingProject


def load():
    try:
        with open("projects.json", "r") as f:
            data = json.load(f)
            projects = {}
            for name, project in data["projects"].items():
                projects[name] = KnittingProject.convert_to_python(project)
            return projects, data["current project"]
    except FileNotFoundError:
        return {}, None


def save(projects, current_project, file_path="projects.json"):
    projects_dict = {}
    for name, project in projects.items():
        projects_dict[name] = project.convert_to_json()

    data = {"current project": current_project, "projects": projects_dict}

    with open(file_path, "w") as f:
        json.dump(data, f)

def delete(projects, name):
    if name in projects:
        del projects[name]
        return True
    return False