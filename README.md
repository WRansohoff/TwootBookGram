# TwootBookGram

This project is a simple scalable web app which produces AI-generated responses to 140-character messages which a user inputs. It is meant as a demonstration of how to deploy a small scalable AI-based web app very cheaply, and as an art project which holds a mirror up to how ordinary people tend to act in pseudonymous online spaces.

Work In Progress: You can demo the web app at [https://twootbookgram.com](https://twootbookgram.com), or check the URL in the latest GitHub Actions build for a link to a static site hosted in S3. I am still writing tests for the CI/CD pipeline, though.

## Tech Stack

There is actually very little permanent infrastructure in this project - the LLM inference is performed in cheap serverless function calls. The frontend is a static page served through AWS CloudFront from S3, and the serverless functions use an ElastiCache Redis instance to perform some basic rate limiting on the inference API.

So even though the model produces barely-passable results fairly slowly, this was a fun and interesting project. Stuffing a 350M-parameter LLM into 2GB of RAM with CPU inference demonstrates that we're getting close to a point where these models can be run cheaply without powerful GPUs.

## Motivation

I got the idea when I decided to read a little bit about what sort of training data goes into modern AI models. Most companies who work on state of the art models are tight-lipped about their training data, but it looks like almost all corpuses contain a significant amount of data which was scraped from social media websites via [the "Common Crawl" project](https://commoncrawl.org/).

Reddit, Facebook, Twitter, LinkedIn...these are all gold mines of human vernacular, and they appear to have been tossed into the data threshers alongside the masses of books, newspapers, research papers, legislative records, corporate emails, etc.

So if we prompt an AI model which was trained on years of social media posts to respond as a typical social media user, we should be able to get a blurry glimpse of how people have treated each other online in the past decade. What could possibly go wrong?

## Disclaimer

The main purpose of this repository is to provide an example of how to set up a scalable LLM web app with CI/CD deployments. I'm looking for a job, and I could use a small cloud infrastructure project to add a little bit of spice to the ol' resume.

This is not intended to be a product, and its output should not be trusted or taken seriously. To be clear: This is a parody, and you should NOT take anything that it prints at face value.

I was not involved in the training or production of this model, and I have not fine-tuned it to clean up its responses. It is an unvarnished reflection of human writings, and while I have attempted to filter out some of the worst kinds of responses that it comes up with, it will curse and it may print things that are offensive or harmful.

Due to the pseudo-random nature of LLM inference, most of what it prints will also be completely wrong or nonsensical. All that it's doing is predicting the most likely next word based on all of the text that it was trained on, and this application prompts it to respond in the cadence of a social media post. There is no fact checking, and any resemblance to real people or places, living or dead, is purely coincidental.

In the words of Kurt Vonnegut (*Cat's Cradle*): "Don't be a fool! Close this book at once! It is nothing but [lies]!"

## Installation

You will need to provide the OPT-350M model yourself; I don't know if I am allowed to distribute it, and it's too large to stuff into a small Git repository anyways. You can find instructions in the `runtime_container/opt-350m/` directory. The CI/CD pipeline automatically downloads and processes the model.

This would probably also work with other PyTorch models that have been configured the HuggingFace pipelines, but I've only tested the opt-350m and opt-2.7b LLMs. The 2.7b-parameter model is too large to fit into AWS Lambda's soft limit of 3GB RAM in their serverless functions.

You can find instructions for quantizing the model in `runtime_container/opt-350m-ov/`.

## Local Testing

Once you have downloaded the model and optionally quantized it, you can test the model inference locally by installing the Python dependencies and running the local test script:

(TODO)

## Cloud Deployment

This repository is also set up with GitHub Actions to run some basic tests and deploy itself as a scalable web app in AWS, providing a simple web frontend instead of a CLI container interface.

(TODO)

### Infrastructure Layout

TODO: Image

TODO: Description

### Configuration

If you fork this repository and want to deploy your own version of the web app, you will need to configure a few things.

#### AWS Account ID

You'll need your own AWS account - (TODO: instructions)

#### AWS / GitHub Actions Access

You'll also need to allow your GitHub repository to claim permissions in your AWS account, by configuring OIDC between the two platforms. (TODO: instructions)

