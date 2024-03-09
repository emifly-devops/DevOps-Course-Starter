terraform {
  required_providers {
    azurerm = {
      source          = "hashicorp/azurerm"
      version         = ">= 3.8"
    }
  }

  backend "azurerm" {}
}

provider "azurerm" {
  features {}
}

data "azurerm_resource_group" "main" {
  name                = var.resource_group_name
}

resource "azurerm_cosmosdb_account" "main" {
  location            = data.azurerm_resource_group.main.location
  name                = "${var.prefix}-${var.cosmos_account_name}"
  offer_type          = "Standard"
  kind                = "MongoDB"
  resource_group_name = data.azurerm_resource_group.main.name

  consistency_policy {
    consistency_level = "Session"
  }

  geo_location {
    failover_priority = 0
    location          = data.azurerm_resource_group.main.location
  }

  backup {
    type              = "Continuous"
    tier              = "Continuous7Days"
  }

  capabilities {
    name              = "EnableServerless"
  }

  capabilities {
    name              = "EnableMongo"
  }
}

resource "azurerm_cosmosdb_mongo_database" "main" {
  account_name        = azurerm_cosmosdb_account.main.name
  name                = "todo_app"
  resource_group_name = data.azurerm_resource_group.main.name

  lifecycle {
    prevent_destroy   = false
  }
}

resource "azurerm_service_plan" "main" {
  location            = data.azurerm_resource_group.main.location
  name                = "${var.prefix}-${var.appservice_plan_name}"
  os_type             = "Linux"
  resource_group_name = data.azurerm_resource_group.main.name
  sku_name            = "F1"
}

resource "azurerm_linux_web_app" "main" {
  location            = data.azurerm_resource_group.main.location
  name                = "${var.prefix}-${var.webapp_name}"
  resource_group_name = data.azurerm_resource_group.main.name
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    always_on = false

    application_stack {
      docker_image    = "${var.dockerhub_username}/todo-app"
      docker_image_tag = "latest"
    }
  }

  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io/v1"
    "MONGO_URI"       = azurerm_cosmosdb_account.main.connection_strings[0]
    "SECRET_KEY"      = var.secret_key
    "OAUTH_CLIENT_ID" = var.oauth_client_id
    "OAUTH_CLIENT_SECRET" = var.oauth_client_secret
  }
}
