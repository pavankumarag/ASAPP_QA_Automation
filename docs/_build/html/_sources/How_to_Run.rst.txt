How to Run
===========

There are two ways to run

Setup
--------

Download the zip, from the root directory run docker-compose

.. code-block::

   docker-compose up -d

   Run the below curl commands

   curl -s -o -  -w "%{http_code}" -X POST -d '{"username": "pavan", "password": "pavan123"}' -H 'Content-Type: application/json' http://localhost:5000/users/register

   curl -s -o -  -w "%{http_code}" -X POST -d '{"username": "pavan", "password": "pavan123"}' -H 'Content-Type: application/json' http://localhost:5000/users/login

.. warning::

   Though this is handled in the code, some descrepencies are seen so running these curls for better test execution. This can be fixed in the product



(1) Standalone
-------------------

Download the zip and framework structure is defined in Pre-requisites section.

.. code-block::
   :linenos:

   python3 -m venv asapp-qa-challenge
   source asapp-qa-challenge/bin/activate
   pip install -r ASAPP_QA_Automation/requirements.txt
   cd ASAPP_QA_Automation

   API functional tests
      - pytest -sv --capture sys --html=api_test_endpoints.html api/tests/endpoint
      - pytest -sv --capture sys --html=api_test_workflows.html api/tests/workflow

   UI tests
      - pytest -sv --capture sys --html=ui_test.html ui/tests

   API Benchmarking
      - pytest --benchmark-save=benchmark benchmark/test_login_api.py
      - pytest --benchmark-compare=0003 --benchmark-json=report.json --benchmark-histogram=benchmark --benchmark-compare-fail=median:0.002 --benchmark-compare-fail=max:0.005 benchmark/test_login_api.py
   
   API Performace
      - locust -f performance/api/login.py --headless -u 100 -r 5

(2) Docker
-------------

.. code-block::

   docker exec -ti qa_auto_challenge_prj-qa-1 bash

   pytest -sv api/tests

.. warning::

   Currently docker selenium and zalenium are crashing in Apple M1 so its recommended to run UI tests in standalone way.