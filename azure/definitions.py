import requests
import json
import urllib
from urllib import quote
import azurerm
import credentials
#from credentials import subscription_id, tenant_id, client_id, secret

subscription_id = credentials.subscription_id
tenant_id = credentials.tenant_id
client_id = credentials.client_id
secret = credentials.secret
print(subscription_id)

def create_cluster(subscription_id, tenant_id, client_id, secret, cluster_name, resource_group_name, nodes, private_key):
  subscriptionId = subscription_id
  Tenant_id = tenant_id
  app_id = client_id
  app_secret = secret
  resourceGroupName = resource_group_name
  resourceName = cluster_name
  #nodes = nodes
  token = azurerm.get_access_token(Tenant_id, app_id, app_secret)

  url = 'https://management.azure.com/subscriptions/{}/resourceGroups/{}/providers/Microsoft.ContainerService/managedClusters/{}?api-version=2018-03-31'.format(quote(subscriptionId), quote(resourceGroupName), quote(resourceName)) 
  mydata = {
	"location": "eastus",
 	"tags": {
    	"tier": "production",
        "archv2": ""
   	},
  	"properties": {
    	"kubernetesVersion": "",
    	"dnsPrefix": cluster_name + "dns1" ,
    	"agentPoolProfiles": [
      	{	
        "name": "nodepool1",
        "count": int(nodes),
        "vmSize": "Standard_B2s",#"Standard_DS1_v2",
        "dnsPrefix": cluster_name + "dns1",
        "storageProfile": "ManagedDisks",
        "osType": "Linux"
      	}
    	],
    	"linuxProfile": {
      	"adminUsername": "azureuser",
      	"ssh": {
        	"publicKeys": [
          	{
            	"keyData": private_key,
         	 }	
       		 ]
      	}
    	},
    	"servicePrincipalProfile": {
      	"clientId": app_id,
      	"secret": app_secret,
    	},
    	"addonProfiles": {},
    	"enableRBAC": False,
 	}	
	}



  headers = {'Authorization': 'Bearer ' + token, "Content-Type": "application/json"}

  #Call REST API
  response = requests.put(url, json.dumps(mydata), headers=headers)
  #print(response.text)
  return (response.text)

