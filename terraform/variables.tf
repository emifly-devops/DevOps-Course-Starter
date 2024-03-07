variable "prefix" {
  description = "The prefix used for all resources in this environment"
  default     = "prod"
}

variable "resource_group_name" {
  description = "The name of the resource group to contain the created resources"
}

variable "cosmos_account_name" {
  description = "The name of the CosmosDB account to be associated with the app database"
}

variable "appservice_plan_name" {
  description = "The name of the app service plan to be associated with the web app"
}

variable "webapp_name" {
  description = "The name of the web app, globally unique within Azure"
}

variable "dockerhub_username" {
  description = "The username associated with the Docker Hub account containing the app container image"
}

variable "secret_key" {
  description = "The Flask session secret key"
  sensitive   = true
}

variable "oauth_client_id" {
  description = "The client ID of the GitHub OAuth app to be used for authentication"
  sensitive   = true
}

variable "oauth_client_secret" {
  description = "The client secret of the GitHub OAuth app to be used for authentication"
  sensitive   = true
}
