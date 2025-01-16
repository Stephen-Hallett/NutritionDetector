data "azurerm_client_config" "current" {}

data "azurerm_subscription" "primary" {}

data "azurerm_resource_group" "rg" {
  name     = "rg-${var.project_id}-${var.env}-nzn-001"
}

resource "azurerm_storage_account" "sa" {
  name                     = "sa${var.env}nzn001"
  resource_group_name      = data.azurerm_resource_group.rg.name
  location                 = data.azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_service_plan" "asp" {
  name                = "asp-${var.project_id}-${var.env}-nzn-001"
  location            = data.azurerm_resource_group.rg.location
  resource_group_name = data.azurerm_resource_group.rg.name
  os_type                = "Linux"
  sku_name = var.sku
}

resource "azurerm_function_app" "fa" {
  name                       = "fa-${var.project_id}-${var.env}-nzn-001"
  location                   = data.azurerm_resource_group.rg.location
  resource_group_name        = data.azurerm_resource_group.rg.name
  app_service_plan_id        = azurerm_service_plan.asp.id
  storage_account_name       = azurerm_storage_account.sa.name
  storage_account_access_key = azurerm_storage_account.sa.primary_access_key
  os_type                    = "linux"
  version                    = "~4"

  site_config {
    cors {
      allowed_origins = ["*"]
    }
  }
}