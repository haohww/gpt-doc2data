import openai
from token_processor import split_string_by_token_length
from file_driver import get_file_string
import asyncio
import json

# Ensure we do not run too many concurent requests
model_rate_limits = 2000
max_concurent_request = int(model_rate_limits * 0.75)
throttler = asyncio.Semaphore(max_concurent_request)


def send_chat(context: dict, request: dict):
    openai.api_key = context['api_key']
    resp = openai.ChatCompletion.create(
        model=context['model'], messages=request, temperature=0.0
    )
    print(request)
    print(resp)
    if len(resp['choices']) > 0:
        for msg in resp['choices']:
            if msg['message']['role'] == 'assistant':
                return msg['message']['content']
    return ""


async def request_question(context: dict, input: str, num_data: int) -> dict:
    system_prompt = context['system_prompts']['question_generator'].format(
        num_data=num_data, language=context["language"]
    )
    request = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': input},
    ]
    return json.loads(send_chat(context, request))

async def generate_questions(context: dict):
    doc_string = get_file_string(context)
    jobs = []
    batches = split_string_by_token_length(context, doc_string)
    num_question = context["num_data"] // len(batches)
    for batch in batches:
        jobs.append(request_question(context, batch, num_question))
    results = await asyncio.gather(*jobs)
    return results
