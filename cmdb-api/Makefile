default: help

test: ## test in local environment
	pytest -s  --html=test-output/test/index.html --cov-report html:test-output/coverage --cov=api tests

clean_test: ## clean test output
	rm -f .coverage
	rm -rf .pytest_cache
	rm -rf test-output


docker_test: ## test all case in docker container
	@echo "TODO"

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' ./Makefile | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
