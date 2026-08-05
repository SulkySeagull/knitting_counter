class KnittingCommands:

    def __init__(self, current_project, on_create_project, on_save, on_delete_project):
        self.on_create_project = on_create_project
        self.on_save = on_save
        self.on_delete_project = on_delete_project
        self.project = current_project
        self.multi_step_convo = None  # Tracks which multi step convo we are in
        self.convo_state = None  # Tracks what part of convo we are in
        self.convo_data = None  # Holds conversation data

    def process_command(self, command):
        if self.multi_step_convo == "creating_project":
            return self.create_new_project(command)

        elif self.multi_step_convo == "deleting_project":
            return self.delete_project(command)

        elif "new project" in command or "create project" in command:
            self.multi_step_convo = "creating_project"
            return self.create_new_project(command)

        elif self.project is None:
            return "There are currently no projects. Please create a new project."

        elif "delete" in command:
            self.multi_step_convo = "deleting_project"
            return self.delete_project(command)

        elif "add row" in command:
            response = self.project.add_row()
            self.on_save()
            return response

        elif "frog row" in command:
            response = self.project.frog_row()
            self.on_save()
            return response

        elif "row count" in command:
            response = self.project.rows_knitted()
            return response

        elif "current project" in command:
            return self.project.name

        else:
            return "pardon?"

    def create_new_project(self, command):
        if self.convo_state == "naming_project":
            self.convo_state = "confirming_project"
            self.convo_data = command
            return (
                "CONSTRAIN GRAMMAR",
                f"This project is called {command}. Do you like this name?",
            )

        elif self.convo_state == "confirming_project":
            if "yes" in command:
                self.on_create_project(self.convo_data)
                self.multi_step_convo = None
                self.convo_state = None
                return f"Created new project {self.convo_data}"
            elif "cancel" in command:
                self.multi_step_convo = None
                self.convo_state = None
                return f"Project creation has been cancelled"
            else:
                # If user doesn't like the name need to add cancel option in
                self.convo_state = "naming_project"
                return "OPEN GRAMMAR", "What would you like to call this project"
        else:
            self.convo_state = "naming_project"
            return "OPEN GRAMMAR", "What would you like to call this project"

    def delete_project(self, command):
        if self.convo_state == "deleting_project":
            self.convo_state = "confirming_deletion"
            self.convo_data = command
            return (
                "CONSTRAIN GRAMMAR",
                f"Are you sure you want to delete {command}?",
            )
        if self.convo_state == "confirming_deletion":
            if "yes" in command:
                result = self.on_delete_project(self.convo_data)
                self.multi_step_convo = None
                self.convo_state = None
                if result:
                    return f"{self.convo_data} has been deleted"
                else:
                    return f"Sorry I couldn't find {self.convo_data} project to delete"

            else:
                # If user doesn't like the name need to add cancel option in
                self.multi_step_convo = None
                self.convo_state = None
                return "Deletion has been cancelled"
        else:
            self.convo_state = "deleting_project"
            return "OPEN GRAMMAR", "Which project would you like to delete?"
