#!/usr/bin/env bash

rm -rf ./allure_results
behave -f allure_behave.formatter:AllureFormatter -o ./allure_results ./features
allure serve ./allure_results