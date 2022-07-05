## Install

### Install requirements
`poetry install`
### Install docker image for janus
`docker pull janusgraph/janusgraph`

## Run
### Run janusgraph docker container
`docker run -it -p 8182:8182 janusgraph/janusgraph`
### Run and verify the FastAPI server
`uvicorn main:app --reload --host 0.0.0.0 --port 8000`