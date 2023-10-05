from .function_idea import FunctionIdea
from .function_project import FunctionProj
from .function_task import FunctionTask

func_idea = FunctionIdea()
func_porj = FunctionProj()
func_task = FunctionTask()

available_functions = {
                "add_idea": func_idea.add_idea,
                "update_idea": func_idea.update_idea,
                "show_all_ideas": func_idea.show_all_ideas,
                "add_project": func_porj.add_project,
                "add_task": func_task.add_task,
                "show_all_projects": func_porj.show_all_projects,
                "show_all_tasks": func_task.show_all_tasks,
                "update_project": func_porj.update_project,
                "update_task": func_task.update_task,
            }