build:
	docker build -t cas-puller .

push:
	docker tag cas-puller image-registry.apps.silver.devops.gov.bc.ca/78c88a-tools/cas-puller
	docker push image-registry.apps.silver.devops.gov.bc.ca/78c88a-tools/cas-puller
