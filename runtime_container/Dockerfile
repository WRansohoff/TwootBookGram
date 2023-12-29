FROM public.ecr.aws/lambda/python:3.10

ARG LLM_FORBIDDEN_WORDS=
ARG REDIS_HOST=

ENV LLM_FORBIDDEN_WORDS $LLM_FORBIDDEN_WORDS
ENV REDIS_HOST $REDIS_HOST

RUN pip install --upgrade pip
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install transformers redis
RUN pip install optimum[openvino,nncf]
RUN pip cache purge

RUN mkdir ${LAMBDA_TASK_ROOT}/opt-350m-ov
COPY opt-350m-ov ${LAMBDA_TASK_ROOT}/opt-350m-ov

COPY lambda_function.py ${LAMBDA_TASK_ROOT}/

# Debug: Drop into a shell in the container when it launches.
#ENTRYPOINT /usr/bin/bash

# Normal entry: Run the Lambda function handler.
CMD [ "lambda_function.handler" ]
