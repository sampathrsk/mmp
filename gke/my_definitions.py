from google.cloud import container_v1

client = container_v1.ClusterManagerClient()

project_id = 'laasprobhu'
zone = 'us-central1-a'

#cluster_name = input("Enter the cluster name:")
#nodes = int(input("Enter the number of nodes:"))
#disksize = int(input("Enter the DiskSize:"))

def gke_create_cluster(cluster_name,nodes,disksize):
  cluster = {
  "name": cluster_name,
      "master_auth": {
        "username": "admin",
      },
      "logging_service": "logging.googleapis.com",
      "monitoring_service": "monitoring.googleapis.com",
      "network": "projects/laasprobhu/global/networks/default",
      "addons_config": {
        "http_load_balancing": {},
        "kubernetes_dashboard": {}
     },
      "subnetwork": "projects/laasprobhu/regions/us-central1/subnetworks/default",
      "node_pools": [
        {
          "name": "default-pool",
          "config": {
            "machine_type": "n1-standard-1",
            "disk_size_gb": disksize,
            "oauth_scopes": [
              "https://www.googleapis.com/auth/compute",
              "https://www.googleapis.com/auth/devstorage.read_only",
              "https://www.googleapis.com/auth/logging.write",
              "https://www.googleapis.com/auth/monitoring",
              "https://www.googleapis.com/auth/servicecontrol",
              "https://www.googleapis.com/auth/service.management.readonly",
              "https://www.googleapis.com/auth/trace.append"
            ],
            "image_type": "COS",
          },
          "initial_node_count": nodes,
          "autoscaling": {},
          "version": "1.10.9-gke.5"
        }
      ],
      "network_policy": {},
      "ip_allocation_policy": {},
      "master_authorized_networks_config": {},
      "initial_cluster_version": "1.10.9-gke.5"
  }
  return cluster

#response = client.create_cluster(project_id, zone, cluster)
#print response


#response = client.delete_cluster(project_id, zone, cluster_name)
#print response
