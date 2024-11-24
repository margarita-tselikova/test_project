# User service test project
The project was created to practice test automation skills. It contains a User service created using Flask, with post/get/put/delete methods, which are covered by various automated tests.

## How to Run Tests (Windows):
1. Clone repo
2. Go to the project directory
3. Prepare environment:
```buildoutcfg
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
4. Start User Service: `python .\service\user_service.py`
5. Run Tests:
   - API: `pytest tests\test_user_api.py` 
   - behave:  `.\features\run_behavior_tests.sh`

__P.S.__ Do not forget to press CTRL+C to quit the service when you're done

