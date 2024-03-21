# Example: Python - Marketing Campaign Actions

This example demonstrates how to create Actions for the [Robocorp Action Server](https://github.com/robocorp/robo/tree/master/action_server/docs#readme) to assist with customer data and marketing campaigns. These Actions can be integrated into automated workflows to enhance marketing strategies, offering a practical way to tailor content and offers to specific customer segments based on product interest.

`Actions` and `Action Server` enable you to "give your AI Agents hands" meaning that your AI/LLM Agent can help your users perform distinct actions that get executed based on the LLM discussion.

## Quickstart

👉 Follow the Action Server [Quickstart guide](https://github.com/robocorp/robocorp?tab=readme-ov-file#%EF%B8%8F-quickstart) in the main repository.


## Dependency management

Dependencies need to be added to [`package.yaml`](package.yaml).

👉 [package.yaml documentation](https://github.com/robocorp/robocorp/blob/master/action_server/docs/guides/01-package-yaml.md) in the main repository.

## Actions in VS Code 

👉 Using [Robocorp Code extension for VS Code](https://marketplace.visualstudio.com/items?itemName=robocorp.robocorp-code), you can get everything set up and running in VS Code in no time.

The template has a few files that enable the extension to find and set up your action environment and provide code completion. There is also a side panel where we have and will add some easy-to-use functionalities.

![](docs/vscode.png)

When debugging your Actions Python code, you probably do not want to give the inputs every time you run and always be running the Action Server. `Robocorp Code` integration allows you to run and debug actions from within VSCode, enabling custom input to be specified as `.json` files.


## What does the example Action do?

This example uses a database with predifined queries that the LLM can call with the suitable parameters without creating any actual DB queries.

We leverage SQLite for database interactions, illustrating that the Python ecosystem offers a wide array of libraries and tools for custom Action development. Explore [PyPI](https://pypi.org/) for additional libraries, including those specific to [Robocorp](https://pypi.org/search/?q=robocorp-), to enhance your Actions further.

🚀 Now, go get'em

