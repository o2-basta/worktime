# Worktime

## Overview

Worktime is a time measuring tool designed to help users track their work activities and manage tasks efficiently. Built using Python, this tool allows you to log work sessions, create subtasks, and generate reports on elapsed work time.

## Features

- Start and end work sessions
- Manage subtasks
- Generate reports of work time
- Integrate with GitHub issues
- Categorize routine tasks like meditation, lunch, and reading
- User-friendly command-line interface

## Installation

To install Worktime, you need to have Python 3.6 or later installed on your system. You can install the package using the following command:

```bash
git clone github.com/o2-basta/worktime.git && cd worktime && python setup.py install
```

or just use pip ( currently not working )

```bash
pip install git+https://github.com/o2-basta/worktime.git
```

Make sure you have the necessary permissions to install packages.

## Usage

You can run the Worktime tool from the command line with various commands. Below are some common usage examples.

### Start a Task

To start a new task, use:

```bash
python worktime.py start
```

You can also start a task with a title:

```bash
python worktime.py start "Task Title"
```

### End a Task

To end the current task, simply run:

```bash
python worktime.py end
```

### Commit Changes

To end the current task and commit your changes to Git:

```bash
python worktime.py commit
```

### View Current Task Status

To check the current status of your work, use:

```bash
python worktime.py status
```

### Start a Subtask

To start a sub-task under the current task, use:

```bash
python worktime.py sub
```

### Reset Work Logs

To reset your work logs and remove all records:

```bash
python worktime.py reset
```

### Help Command

For additional commands and information, you can use:

```bash
python worktime.py help
```

## Working with GitHub Issues

If you want to start a task related to a GitHub issue, simply run:

```bash
python worktime.py issue #issue_number
```

Make sure you have the GitHub CLI (`gh`) installed and authenticated on your system.

## Example Session

1. Start a task:
   ```bash
   python worktime.py start "Develop feature X"
   ```

2. Create a subtask:
   ```bash
   python worktime.py sub
   ```

3. End the task:
   ```bash
   python worktime.py end
   ```

4. Commit the changes:
   ```bash
   python worktime.py commit
   ```

## Author

**Taiho Lee**
Email: basta@opentutorials.org
GitHub: [Taiho Lee](https://github.com/o2-basta/worktime)

## License

This project is licensed under the [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) license.

## Contributing

Feel free to fork the repo and create pull requests for any improvements or bugs you find!
```

This README provides a concise yet detailed overview of the Worktime project, including installation instructions, command usage, and basic features. Adjust any sections according to your personal preferences or additional details specific to the project.

## Overview

Worktime is a time measuring tool designed to help users track their work activities and manage tasks efficiently. Built using Python, this tool allows you to log work sessions, create subtasks, and generate reports on elapsed work time.

## Features

- Start and end work sessions
- Manage subtasks
- Generate reports of work time
- Integrate with GitHub issues
- Categorize routine tasks like meditation, lunch, and reading
- User-friendly command-line interface

## Installation

To install Worktime, you need to have Python 3.6 or later installed on your system. You can install the package using the following command:

```bash
pip install .
```

Make sure you have the necessary permissions to install packages.

## Usage

You can run the Worktime tool from the command line with various commands. Below are some common usage examples.

### Start a Task

To start a new task, use:

```bash
python worktime.py start
```

You can also start a task with a title:

```bash
python worktime.py start "Task Title"
```

### End a Task

To end the current task, simply run:

```bash
python worktime.py end
```

### Commit Changes

To end the current task and commit your changes to Git:

```bash
python worktime.py commit
```

### View Current Task Status

To check the current status of your work, use:

```bash
python worktime.py status
```

### Start a Subtask

To start a sub-task under the current task, use:

```bash
python worktime.py sub
```

### Reset Work Logs

To reset your work logs and remove all records:

```bash
python worktime.py reset
```

### Help Command

For additional commands and information, you can use:

```bash
python worktime.py help
```

## Working with GitHub Issues

If you want to start a task related to a GitHub issue, simply run:

```bash
python worktime.py issue #issue_number
```

Make sure you have the GitHub CLI (`gh`) installed and authenticated on your system.

## Example Session

1. Start a task:
   ```bash
   python worktime.py start "Develop feature X"
   ```

2. Create a subtask:
   ```bash
   python worktime.py sub
   ```

3. End the task:
   ```bash
   python worktime.py end
   ```

4. Commit the changes:
   ```bash
   python worktime.py commit
   ```

## Author

**Taiho Lee**
Email: basta@opentutorials.org
GitHub: [Taiho Lee](https://github.com/o2-basta/worktime)

## License

This project is licensed under the [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) license.

## Contributing

Feel free to fork the repo and create pull requests for any improvements or bugs you find!
```

This README provides a concise yet detailed overview of the Worktime project, including installation instructions, command usage, and basic features. Adjust any sections according to your personal preferences or additional details specific to the project.