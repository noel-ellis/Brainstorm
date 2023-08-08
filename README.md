# Philosophy
- Turn ideas into actions, then manage them
- Notes are used to brainstorm ideas, todo lists are used to manage their execution. 
- Smooth transition between the two is crucial
# Features
## Core
### Accounts
- email activation
### Folders
- multilevel
- colors/icons
- tags
### Todo lists
> Should projects have unique names? Considering the planned voice assistant
- attached to a folder
- flexible:
	- pull tasks from every note inside the parent folder
	- can contain tasks of their own
- priority (list-specific)
- due date (*optional*)
- named after the parent folder by default 
### Notes
> Should note tasks be differentiated by the notes they attached to? ***Yes, it's reflected in the db***
> How to trace some line in the note to its Task object?***Markdown contains ==task_id== and not the title***
- markdown
- tags
- tasks can be created inside a note; they are associated with a folder's todo list 
- pin
### Tasks
- always attached to a todo list
- optionally attached to a note
- priority (task-specific, local for the parent todo list)
- subtasks
- due date (*optional*)
- can be completed/failed
- open/closed status via optional timestamp
## Measurements
### Timers
- strictly attached to a task
- measures task performance time
### Task Due Date History
- measures task due date changes
- records timestamps
### Task Priority History
- measures task priority changes
- records timestamps
### Todo List Due Date History
- measures todo list due date changes
- records timestamps
### Todo List Priority History
- measures todo list priority changes
- records timestamps
### 🚧 Habits
> How do I create a habit? ***From a task OR latest task out of a list of ones***
> How does a new task spawn? ***clones the previous one***
> How does it change related tasks? ***doesn't change them***
> What if a task is attached to a note? ***add a new one next the previous one, differentiate by date***
> What if a task has a parent? ***detach*** 🚧
> What happens when the parent task closes? ***no parent tasks***
> Can task's due date change? ***Yes***
> 
- task factory
- ties all related tasks together, allowing habit-specific measurements
## Dashboards
### Activities Tab
- Browse through all todo lists, sorted and filtered
- Add specific tasks or whole lists to Focus Tab
### Focus Tab
- Contains relevant tasks/projects for today
### 🚧 Performance Tab
> What exact metrics?
> How is the data represented?
- contains all the metrics on a timeline
## Planned
### 🚧 Voice Assistant
- create new projects (folders with todo lists), dictate documents, and add new tasks
- add lists/tasks to focus 
- ask for metrics
# STACK
- django
- postgres
- tailwind
