from transformers import AutoTokenizer, set_seed, pipeline, AutoModelForCausalLM
from optimum.intel import OVModelForCausalLM

import json
import os
import random
import redis
import torch

model_path = 'opt-350m-ov'
ModelClass = OVModelForCausalLM

# This is a list of words that the model is not allowed to print.
# This will not prevent the model from printing offensive sentiments,
# but it should block some of the worst things it could say.
# Fill in your own list here by building the container with
# an "LLM_FORBIDDEN_WORDS" build argument containing a space-separated
# list of substrings to avoid printing.
bad_words = os.getenv('LLM_FORBIDDEN_WORDS', default='').split()

# Rate-limiting cache host.
# If not defined, rate limiting will be disabled.
cache_host = os.getenv('REDIS_HOST', default='')

def handler(event, context):
  # Fetch a list of dictionary words.
  # (Small random subset of /usr/share/dict/words)
  with open('username_words.txt', 'r') as dict_words:
    words = dict_words.read().split()

  print('Loaded words')

  # Temporary debug - has event format changed?
  print(f'{event}')

  # Perform rate-limiting if a cache is configured.
  if cache_host:
    cache = redis.Redis(host=cache_host, port=6379, decode_responses=True)
    try:
        from_ip = event['headers']['x-forwarded-for']
        rl_key = f'{from_ip}:LLM'
        cache.setnx(rl_key, 10)
        cache.expire(rl_key, 600)
        cache.decrby(rl_key, 1)
        if int(cache.get(rl_key)) <= 0:
          return { 'responses': [{
            'response': '<rate limit exceeded, please try again later>',
            'user': '<System>'
          }]}
    except KeyError:
        # If no referral IP is available, fall back to a system-wide rate limit.
        rl_key = f'SYSTEMLIMIT:LLM'
        cache.setnx(rl_key, 128)
        cache.expire(rl_key, 600)
        cache.decrby(rl_key, 1)
        if int(cache.get(rl_key)) <= 0:
          return { 'responses': [{
            'response': '<system-wide rate limit exceeded, please try again later>',
            'user': '<System>'
          }]}
  else:
    print('Warning: no rate-limiting cache configured.')

  # Check that the input string is not too long.
  body = json.loads(event['body'])
  post = body['input']
  if len(post) > 150:
    return { 'responses': ['<your input was too long to process. (150 character limit)>'] }

  # Set the PRNG seed for text generation.
  set_seed(int(random.random()*256))

  # Create the LLM inference pipeline object.
  model = ModelClass.from_pretrained(model_path, use_cache=False)
  tokenizer = AutoTokenizer.from_pretrained(model_path)
  generator=pipeline('text-generation',
                     model=model,
                     tokenizer=tokenizer,
                     do_sample=True,
                     low_memory=True,
                     min_new_tokens=15,
                     max_new_tokens=45,
                     repetition_penalty=1.2)

  print('Loaded generator')

  #prompt = f'The following is a discussion from a social media website. Post: "{tweet}". Response: '
  #prompt = f'"{post}". The response to this social media post is: '
  #prompt = f'Social media post: "{post}". Social media response: "@'
  #prompt = f'This is a social media post, followed by a reply. The reply is a helpful attempt to answer the user. Post: "{post}". Reply: @'
  prompt = f'A social media user posted: "{post}".\nIn reply, another user posted: '
  #prompt_end = 'Response: '
  #prompt_end = 'post is: '
  #prompt_end = 'response: '
  #prompt_end = 'Reply: '
  prompt_end = 'posted: '

  # Produce and filter three generated responses from the AI model.
  responses = []
  for i in range(3):
    # Response
    gen_resp = generator(prompt)
    resp = gen_resp[0]['generated_text']
    #print(resp)
    sind = resp.rfind(prompt_end) + len(prompt_end)
    resp = resp[sind:]
    #print(resp)

    # Optional: limit response to a specific length.
    # Default: one gross of characters
    max_len = 144
    if len(resp) > max_len:
      resp = resp[:max_len]

    #print(resp)
    # Try not to end a generated post in the middle of a clause.
    lind = max(
      resp.rfind('.'),
      resp.rfind(','),
      resp.rfind('?'),
      resp.rfind('!'),
      resp.rfind('\n')
    )

    if lind > 0:
      resp = resp[:lind+1]
    resp = resp.strip('"')

    filter_resp = resp.lower()
    for bw in bad_words:
      if bw in filter_resp:
        resp = "<The model generated a response that was too offensive to print. Sorry.>"
        break

    resp = resp.strip()
    if resp[0] == '>':
      resp = resp[1:]
    resp = resp.replace('\\u2019', "'")

    # Generate a random username from dictionary words.
    username = words[int(random.random()*len(words))]
    style = random.random()
    if style > 0.75:
      part1 = words[int(random.random()*len(words))]
      part2 = words[int(random.random()*len(words))]
      username = f'{part1}{part2}'
    elif style > 0.5:
      part1 = words[int(random.random()*len(words))]
      part2 = words[int(random.random()*len(words))]
      username = f'{part1}_{part2}'
    elif style > 0.25:
      part1 = words[int(random.random()*len(words))]
      part2 = words[int(random.random()*len(words))]
      part3 = words[int(random.random()*len(words))]
      username = f'{part1}_{part2}{part3}'

    responses.append({'response': resp, 'user': username})
    print(f'Response {i} done.')

  # Return the generated responses.
  return {
    'responses': responses
  }
