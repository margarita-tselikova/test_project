#!/usr/bin/env python

behave -f allure_behave.formatter:AllureFormatter -o ./features/allure_results ./features
allure serve ./features/allure_results