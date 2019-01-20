.PHONY: destroy
destroy:
	cd vagrant && vagrant destroy -f && cd ..

.PHONY: up
up:
	cd vagrant && grep config.vm.define Vagrantfile | awk -F'"' '{print $$2}' | xargs -P4 -I {} vagrant up {} && cd ..