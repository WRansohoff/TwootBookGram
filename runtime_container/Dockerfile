FROM public.ecr.aws/lambda/python:3.10

ARG LLM_FORBIDDEN_WORDS=
ARG REDIS_HOST=

ENV LLM_FORBIDDEN_WORDS $LLM_FORBIDDEN_WORDS
ENV REDIS_HOST $REDIS_HOST
ENV CI "true"

RUN pip install --upgrade pip
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install transformers redis
RUN pip install --upgrade-strategy eager optimum[openvino,nncf,onnxruntime]
RUN pip cache purge

RUN mkdir ${LAMBDA_TASK_ROOT}/opt-350m-ov
COPY opt-350m-ov ${LAMBDA_TASK_ROOT}/opt-350m-ov

COPY username_words.txt ${LAMBDA_TASK_ROOT}/

COPY lambda_function.py ${LAMBDA_TASK_ROOT}/

# Debug: Drop into a shell in the container when it launches.
#ENTRYPOINT /usr/bin/bash

# Normal entry: Run the Lambda function handler.
CMD [ "lambda_function.handler" ]
