update_description = """
    update the idea, conception, thought or some summaried after user \
    confirm to update the content.

    collection the previous idea and new idea from the conversation

    the previous idea and new idea without any sequence number.
"""

function_list = [
    {
        "name": "add_project",
        "description": "add project after user confirm creatation down",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the project"
                },
                "description": {
                    "type": "string",
                    "description": "The description of the project"
                }
            },
        "required": ["name", "description"],
        },
    },

    {
        "name": "show_all_projects",
        "description": "show all the projects' name",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "add_task",
        "description": "add task which must be related to one project after user confirm creatation down",
        "parameters": {
            "type": "object",
            "properties": {
                "description": {
                    "type": "string",
                    "description": "The description of the task",
                },
                "project_name": {
                    "type": "string",
                    "description": "The name of the project",
                },
            },
        "required": ["description", "project_name"],
        },
    },

    {
        "name": "show_all_tasks",
        "description": "show all the tasks wich are belong to the specific project",
        "parameters": {
            "type": "object",
            "properties": {
                "project_name": {
                    "type": "string",
                    "description": "the name of the project",
                },
            },
        "required": ["project_name"],
        },
    },

    {
        "name": "add_idea",
        "description": "add the idea, conception, thought or some summaried after user confirm creatation down",
        "parameters": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The content of the idea"
                }
            },
        "required": ["content"]
        },
    },

    {
        "name": "update_idea",
        # "description": "update the idea, conception, thought or some summaried after user confirm to update the content",
        "description": update_description,
        "parameters": {
            "type": "object",
            "properties": {
                "previous_idea": {
                    "type": "string",
                    "description": "The content of previous idea"
                },
                "new_idea": {
                    "type": "string",
                    "description": "The content of new idea"
                },
            },
        "required": ["previous_idea", "new_idea"]
        }
    },

    {
        "name": "show_all_ideas",
        "description": "show all the ideas",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
]

