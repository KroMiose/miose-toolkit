from typing import Tuple


async def get_reply(question_text) -> str:
    res, _ = await gen_chat_response_text(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT.strip()},
            {"role": "user", "content": question_text.strip()},
        ],
    )
    return res


async def gen_chat_response_text(
    messages,
    temperature: float = 0.1,
    frequency_penalty: float = 0.2,
    presence_penalty: float = 0.2,
    top_p=1,
    model="gpt-3.5-turbo",
) -> Tuple[str, int]:
    """生成聊天回复内容"""

    response = await openai.ChatCompletion.acreate(
        model=model,
        messages=messages,
        temperature=temperature,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        top_p=top_p,
    )
    # logger.debug(response)
    output = response["choices"][0]["message"]["content"]  # type: ignore
    token_consumption = response["usage"]["total_tokens"]  # type: ignore
    return output, token_consumption  # noqa: RET504
