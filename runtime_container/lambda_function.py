from transformers import AutoTokenizer, set_seed, pipeline, AutoModelForCausalLM
from optimum.intel import OVModelForCausalLM

import json
import random
import redis
import torch

model_path = 'opt-350m-ov'
ModelClass = OVModelForCausalLM

# This is a list of words that the model is not allowed to print.
# This will not prevent the model from printing offensive sentiments,
# but it should block some of the worst things it could say.
# Fill in your own list here; I don't want Microsoft banning my
# GitHub account because it contains naughty words.
bad_words = [
]

def handler(event, context):
  cache = redis.Redis(host='llmratelimitcache-qw55fm.serverless.use2.cache.amazonaws.com', port=6379, decode_responses=True, ssl=True)
  from_ip = event['headers']['x-forwarded-for']
  #from_ip = 'localhost'
  rl_key = f'{from_ip}:LLM'
  cache.setnx(rl_key, 10)
  cache.expire(rl_key, 600)
  cache.decrby(rl_key, 1)
  if int(cache.get(rl_key)) <= 0:
    return { 'responses': ['<rate limit exceeded, please try again later>'] }

  body = json.loads(event['body'])
  post = body['input']
  if len(post) > 150:
    return { 'responses': ['<your input was too long to process. (150 character limit)>'] }

  set_seed(int(random.random()*256))

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

  responses = []
  for i in range(3):
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
    responses.append(resp)

  return {
    'responses': responses
  }
