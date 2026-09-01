#!/usr/bin/env bash
# The same thing, the way you'd actually write it. This is the slide.
set -e

az group create --name byoiac-demo --location eastus --tags env=demo talk=kcdc

az storage account create --name byoiacdemo2026 --resource-group byoiac-demo \
  --location eastus --sku Standard_LRS --kind StorageV2 --allow-blob-public-access true

az storage container create --name files --account-name byoiacdemo2026 --public-access blob

echo '<h1>Deployed by one dumb script</h1><p>KCDC 2026 - Build Your Own IaC</p>' > hello.html
az storage blob upload --account-name byoiacdemo2026 --container-name files \
  --name hello.html --file hello.html --content-type text/html --overwrite

echo "https://byoiacdemo2026.blob.core.windows.net/files/hello.html"
