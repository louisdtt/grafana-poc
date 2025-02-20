# App
helm install app ./helm -n app
helm upgrade app ./helm -n app

# Ingress
minikube addons enable ingress
minikube tunnel
echo "127.0.0.1 chart-example.local" | sudo tee -a /etc/hosts > /dev/null

# Alloy
kubectl create namespace grafana

helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install --namespace grafana alloy grafana/alloy

# VictoriaMetrics
kubectl create namespace victoria
helm repo add vm https://victoriametrics.github.io/helm-charts/
helm repo update

helm show values vm/victoria-metrics-k8s-stack > values.yaml
helm install vmks vm/victoria-metrics-k8s-stack -f values.yaml -n victoria
k get secret --namespace victoria vmks-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

# VictoriaLogs

helm show values vm/victoria-logs-single > values.yaml
helm install vls vm/victoria-logs-single -f values.yaml -n victoria