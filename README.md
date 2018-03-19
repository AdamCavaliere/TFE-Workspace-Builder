# TFE-Workspace-Builder

## Purpose
Utilize to interact with Terraform Enterprise environments to build out your workspace.

This will consume the variables.tf file to auto populate the variables you have defined, and will even populate the default values.

The envVars.json file is there to setup API keys, and other keys that are typically utilized in your workspaces. It is setup to create not only environment variables, but also regular terraform variables that are may be utilized by a provider. 

## Current Activity / Notes
Currently, Vault integration is being worked on to support storing these secrets, rather than storing them in a JSON file.
