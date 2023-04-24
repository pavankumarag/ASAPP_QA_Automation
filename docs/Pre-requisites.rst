Pre-requisites
===============
Download the zip

framework structure as below

.. code-block::

   qa_auto_challenge_prj
      /src
         /api
            Dockerfile
         /ui
            Dockerfile
      /ASAPP_QA_Automation
         Dockerfile
      docker-compose.yml


(1)  Build the Images for API and UI:

.. code-block::

    docker build ./src/api -t asapp-qa-challenge-api
    
    docker build ./src/ui -t asapp-qa-challenge-ui

(2) Build the image for QA automation framework

.. code-block::

   docker build ./ASAPP_QA_Automation -t asapp-qa-challenge-qa