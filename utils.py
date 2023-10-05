from function import available_functions

class FunctionExcHelp:
    def __init__(self, session, method_name, method_args, indexdb) -> None:
        self.available_functions = available_functions
        self.session = session
        self.method_name = method_name
        self.func_args = method_args
        self.function = self.available_functions[method_name]
        self.indexdb = indexdb

    def run(self):
        match self.method_name:
            case "show_all_ideas":
                print("show_all_ideas")
                return self.function(session=self.session)
            case "show_all_projects":
                print("show_all_projects")
                return self.function(session=self.session)
            case "add_idea":
                print("add_idea")

                return self.function(
                    session = self.session,
                    content = self.func_args["content"],
                    index = self.indexdb.idea_index,
                )
            case "update_idea":
                print("update_idea")

                return self.function(
                    session = self.session,
                    previous_idea = self.func_args["previous_idea"],
                    new_idea = self.func_args["new_idea"],
                    index = self.indexdb.idea_index,
                )
            case "add_project":
                print("add_project")
                return self.function(
                    session = self.session,
                    name = self.func_args["name"],
                    description = self.func_args["description"],
                    nindex = self.indexdb.proj_n_index,
                    dindex = self.indexdb.proj_d_index,
                )
            case "add_task":
                print("add_task")

                return self.function(
                    session = self.session,
                    project_name = self.func_args["project_name"],
                    description = self.func_args["description"],
                    tindex = self.indexdb.task_index,
                    pnindex = self.indexdb.proj_n_index,
                )
            case "show_all_tasks":
                print("show_all_tasks")

                return self.function(
                    session = self.session,
                    project_name = self.func_args["project_name"],
                    pnindex = self.indexdb.proj_n_index,
                )
            case "update_project":
                print("update_project")

                return self.function(
                    session = self.session,
                    project_name = self.func_args["project_name"],
                    values = self.func_args,
                )
            case "update_task":
                print("update_task")

                return self.function(
                    session = self.session,
                    description = self.func_args["description"],
                    project_name = self.func_args["project_name"],
                    tindex = self.indexdb.task_index,
                    pnindex = self.indexdb.proj_n_index,
                    values = self.func_args,
                )
