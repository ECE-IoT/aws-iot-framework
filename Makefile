BASE := $(shell /bin/pwd)
CODE_COVERAGE = 72

#############
#  SAM vars	#
#############

target:
	$(info ${HELP_MESSAGE})
	@exit 0

clean: ##=> Deletes current build environment and latest build
	$(info [*] Who needs all that anyway? Destroying environment....)
	rm -rf ./.aws-sam/

build: ##=> Same as package except that we don't create a ZIP
	sam build

deploy.guided: ##=> Guided deploy that is typically run for the first time only
	sam deploy --guided

deploy: ##=> Deploy app using previously saved SAM CLI configuration
	sam deploy

hurry: ##=> Run full workflow for the first time
	$(MAKE) build
	$(MAKE) deploy.guided

#############
#  Helpers  #
#############

define HELP_MESSAGE
	Environment variables to be aware of or to hardcode depending on your use case:

	NETWORK
		Default: ""
		Info: Docker Network to connect to when running Lambda function locally

	Common usage:

	...::: Cleans up the environment - Deletes Virtualenv, ZIP builds and Dev env :::...
	$ make clean

	...::: Builds Lambda function dependencies:::...
	$ make build

	...::: Deploy for the first time :::...
	$ make deploy.guided

	...::: Deploy subsequent changes :::...
	$ make deploy

	...::: Deploy subsequent changes :::...
	$ make hurry

endef
