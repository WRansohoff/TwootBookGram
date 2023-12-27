FROM public.ecr.aws/lambda/python:3.10

RUN pip install --upgrade pip && \
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu && \
    pip install transformers redis && \
    pip install --upgrade-strategy eager optimum[openvino,nncf,onnxruntime] && \
    pip cache purge

RUN mkdir ${LAMBDA_TASK_ROOT}/opt-350m-ov
COPY opt-350m-ov ${LAMBDA_TASK_ROOT}/opt-350m-ov

COPY lambda_function.py ${LAMBDA_TASK_ROOT}/

# Debug: Drop into a shell in the container when it launches.
#ENTRYPOINT /usr/bin/bash

# Normal entry: Run the Lambda function handler.
CMD [ "lambda_function.handler" ]
