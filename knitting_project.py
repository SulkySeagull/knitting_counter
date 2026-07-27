import json


class KnittingProject:

    def __init__(self, name):
        self.name = name
        self.row_count = 0
        self.file_path = f"{name}.json"

    def rows_knitted(self):
        print(f"Knitted {self.row_count} rows so far")

    def add_row(self):
        self.row_count += 1

    def add_multiple_rows(self, num_rows):
        self.row_count += num_rows

    def frog_row(self):
        # Making sure row count doesn't go into negative
        if self.row_count >= 1:
            self.row_count -= 1

    def frog_multiple_rows(self, num_rows):
        # Making sure row count doesn't go into negative
        if self.row_count - num_rows >= 0:
            self.row_count -= num_rows

    def convert_to_json(self):
        return {"name": self.name, "row_count": self.row_count}

    @classmethod
    def convert_to_python(cls, json_data):
        project = KnittingProject(json_data["name"])
        project.row_count = json_data["row_count"]
        return project
