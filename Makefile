# path of the file to upload to gcp (the path of the file should be absolute or should match the directory where the make command is run)
LOCAL_PATH=merged.csv
# project id
PROJECT_ID=le-wagon-batch-713
# bucket name
BUCKET_NAME=wagon-data-713-velasquez
# bucket directory in which to store the uploaded file (we choose to name this data as a convention)
BUCKET_FOLDER=data
# name for the uploaded file inside the bucket folder (here we choose to keep the name of the uploaded file)
# BUCKET_FILE_NAME=another_file_name_if_I_so_desire.csv
BUCKET_FILE_NAME=$(shell basename ${LOCAL_PATH})
REGION=europe-west1
set_project:
	-@gcloud config set project ${PROJECT_ID}
create_bucket:
	-@gsutil mb -l ${REGION} -p ${PROJECT_ID} gs://${BUCKET_NAME}
upload_data:
	-@gsutil cp ${LOCAL_PATH} gs://${BUCKET_NAME}/${BUCKET_FOLDER}/${BUCKET_FILE_NAME}
### GCP configuration - - - - - - - - - - - - - - - - - - -
# /!\ you should fill these according to your account
### GCP Project - - - - - - - - - - - - - - - - - - - - - -
# not required here
### GCP Storage - - - - - - - - - - - - - - - - - - - - - -
# BUCKET_NAME=XXX
##### Data  - - - - - - - - - - - - - - - - - - - - - - - -
# not required here
##### Training  - - - - - - - - - - - - - - - - - - - - - -
# will store the packages uploaded to GCP for the training
BUCKET_TRAINING_FOLDER = 'trainings'
##### Model - - - - - - - - - - - - - - - - - - - - - - - -
# not required here
### GCP AI Platform - - - - - - - - - - - - - - - - - - - -
##### Machine configuration - - - - - - - - - - - - - - - -
# REGION=europe-west1
PYTHON_VERSION=3.7
FRAMEWORK=scikit-learn
RUNTIME_VERSION=2.2
##### Package params  - - - - - - - - - - - - - - - - - - -
PACKAGE_NAME=linkedin_project
FILENAME=trainer
##### Job - - - - - - - - - - - - - - - - - - - - - - - - -
JOB_NAME=linkedin_project_training_pipeline_$(shell date +'%Y%m%d_%H%M%S')

# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt

check_code:
	@flake8 scripts/* linkedin_project/*.py

black:
	@black scripts/* linkedin_project/*.py

test:
	@coverage run -m pytest tests/*.py
	@coverage report -m --omit="${VIRTUAL_ENV}/lib/python*"

ftest:
	@Write me

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr linkedin_project-*.dist-info
	@rm -fr linkedin_project.egg-info

install:
	@pip install . -U

all: clean install test black check_code

count_lines:
	@find ./ -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./scripts -name '*-*' -exec  wc -l {} \; | sort -n| awk \
		        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./tests -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''

# ----------------------------------
#      UPLOAD PACKAGE TO PYPI
# ----------------------------------
PYPI_USERNAME=<AUTHOR>
build:
	@python setup.py sdist bdist_wheel

pypi_test:
	@twine upload -r testpypi dist/* -u $(PYPI_USERNAME)

pypi:
	@twine upload dist/* -u $(PYPI_USERNAME)

run_streamlit:
	streamlit run app.py

gcp_submit_training:
	gcloud ai-platform jobs submit training ${JOB_NAME} \
		--job-dir gs://${BUCKET_NAME}/${BUCKET_TRAINING_FOLDER} \
		--package-path ${PACKAGE_NAME} \
		--module-name ${PACKAGE_NAME}.${FILENAME} \
		--python-version=${PYTHON_VERSION} \
		--runtime-version=${RUNTIME_VERSION} \
		--region ${REGION} \
		--scale-tier custom \
		--master-machine-type n1-highmem-32 \
		--stream-logs

run_api:
	uvicorn api.fast:app --reload  # load web server with code autoreload
