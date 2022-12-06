venv = ../venv
bin = ${venv}/bin/

vault-password=--vault-password-file ansible/vault-password
env-opts=-i ansible/environments/$(env)/hosts -e @ansible/environments/$(env)/secrets

export ANSIBLE_CONFIG = ansible/ansible.cfg

install:
	${bin}pip install -U pip wheel
	${bin}pip install ansible
	${bin}ansible --version

ping:
	${bin}ansible ${vault-password} ${env-opts} web -m ping

secrets:
	${bin}ansible-vault edit ${vault-password} ansible/environments/$(env)/secrets

provision:
	${bin}ansible-playbook ${vault-password} ${env-opts} -t provision ansible/playbook.yml $(extra_opts)

deploy:
	${bin}ansible-playbook ${vault-password} ${env-opts} -t deploy ansible/playbook.yml $(extra_opts)

initdata:
	${bin}ansible-playbook ${vault-password} ${env-opts} -t initdata ansible/playbook.yml $(extra_opts)

dedupe-tags:
	${bin}ansible-playbook ${vault-password} ${env-opts} -t dedupe-tags ansible/playbook.yml $(extra_opts)
