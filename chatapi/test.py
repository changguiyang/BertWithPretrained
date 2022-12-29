
openai_key = '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'
import os
import openai
openai.api_key = openai_key
try:
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="帮我生成2轮中文日常对话",
        temperature=0.31,
        max_tokens=4000,
        top_p=0.3,
        frequency_penalty=0,
        presence_penalty=0
    )
    text = response.get("choices")[0]["text"]
    print(text)
except:
    print("error")
