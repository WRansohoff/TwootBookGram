# Quantized OPT-350m LLM

Once you have downloaded the base `opt-350m` model into `../opt-350m/`, run the following command in this directory:

`optimum-cli export openvino --model ../opt-350m/ --int8 --task text-generation --cache_dir ./model_cache/ ./`

This will quantize the model's weights into 8-bit integers, which lets us generate text more quickly with less memory. If you skip this step, even this small language model will not fit into AWS Lambda's soft limit of 3008MB RAM. With 8-bit weights, the model will almost always run successfully with a mere 2048MB of RAM.

The OpenVINO format quantizes the model weights in a way that allows a CPU to take advantage of the size reduction. Most other quantization schemes that I looked at required a GPU to run the post-quantization model. (AutoAWQ, AutoGPTQ, bitsandbytes, ONNX...)

By compressing the model in a way that lets it run without a GPU, we retain the ability to run it in a cheap serverless cloud function.
