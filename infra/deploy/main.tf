data "azurerm_client_config" "current" {}

data "azurerm_subscription" "primary" {}

data "azurerm_resource_group" "rg" {
  name     = "rg-${var.project_id}-${var.env}-nzn-001"
  location = "${var.location}"
}