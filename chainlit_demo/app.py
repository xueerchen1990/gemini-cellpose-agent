import os
import chainlit as cl
import google.generativeai as genai
from gemini_cell_agent.utils import exec_code, append_image_metadata
from gemini_cell_agent.sys_prompt import pkg_sys_prompt

import datetime

context_file = genai.upload_file(path='../data/cellpose.txt')
sys_prompt = pkg_sys_prompt('cellpose')

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model_name = "gemini-1.5-flash"
config = genai.GenerationConfig(temperature=0)

# Create a cache with a 5 minute TTL
cache = genai.caching.CachedContent.create(
    model=f'models/{model_name}-001',
    display_name='cellpose github repo content', # used to identify the cache
    system_instruction=sys_prompt,
    contents=[context_file],
    ttl=datetime.timedelta(minutes=10),
)

model = genai.GenerativeModel.from_cached_content(cached_content=cache, generation_config=config)
@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="What is cellpose?",
            message="What is cellpose?",
            icon="/public/idea.svg",
            ),

        cl.Starter(
            label="Explain how cell image segmentation works in cellpose.",
            message="Explain how cell image segmentation works in cellpose.",
            icon="/public/learn.svg",
            ),
        cl.Starter(
            label="Write python code to segment a cell image.",
            message="Write python code to segment a cell image.",
            icon="/public/terminal.svg",
            ),
        ]

@cl.on_chat_start
def start_chat():
    cl.user_session.set(
        "chat_history",
        [],
    )

@cl.on_message
async def main(message: cl.Message):
    chat_history = cl.user_session.get("chat_history")
    #print(chat_history)
    msg = cl.Message(content="")

    input_msg = message.content + f'\n\n Remember for coding tasks, please review the correct and wrong coding examples before generating the code.'
    input_msg = append_image_metadata(message)
    if isinstance(input_msg, list):
        input_msg[0] = f'{input_msg[0]}\nAttached image path: {message.elements[0].path}'
    for response in model.start_chat(history=chat_history).send_message(input_msg, stream=True):
        await msg.stream_token(response.text)

    if isinstance(input_msg, list):
        input_msg = input_msg[0]
    chat_history.append({"role": "user", "parts": input_msg})
    chat_history.append({"role": "model", "parts": msg.content})
    await msg.send()

    while True:
        if "```python" not in msg.content:
            break
        res = await cl.AskActionMessage(
            content="Execute code?",
            actions=[
                cl.Action(name="continue", value="continue", label="✅ Yes, execute the code ..."),
                cl.Action(name="cancel", value="cancel", label="❌ No, don't execute the code."),
            ],
        ).send()

        if res and res.get("value") == "continue":
            # Execute the code
            code = msg.content.split("```python")[1].split("```")[0]
            if 'plt.show()' in code:
                code = code.replace('plt.show()', 'plt.savefig("output.png")')
            # Execute the code
            # catch code execution error message
            print('executing the generated code ...')
            captured_output, error_message = exec_code(code)
            print('code execution done')
            if error_message:
                await cl.Message(
                    content=error_message,
                ).send()

                debug_res = await cl.AskActionMessage(
                    content="Debug the code?",
                    actions=[
                        cl.Action(name="debug", value="debug", label="🛠️ Yes, debug the code ..."),
                        cl.Action(name="cancel", value="cancel", label="❌ No, don't debug the code."),
                    ],
                ).send()

                if debug_res and debug_res.get("value") == "debug":
                    # Send the error message to the LLM for debugging
                    debug_input = f"Error: {error_message}\n\nType and shape of the vars in the code:\n{captured_output}\n\nCode:\n{code}"
                    msg = cl.Message(content="")
                    for response in model.start_chat(history=chat_history).send_message(debug_input, stream=True):
                        await msg.stream_token(response.text)
                    chat_history.append({"role": "user", "parts": debug_input})
                    chat_history.append({"role": "model", "parts": msg.content})
                    await msg.send()
                else:
                    await cl.Message(
                        content="Ok, I won't debug the code.",
                    ).send()
                    break  # Exit the loop if user chooses not to debug
            else:
                await cl.Message(
                    content="Here is the output:",
                    elements=[
                        cl.Image(name="image1", display="inline", path="output.png", size="large"),
                    ],
                ).send()
                break  # Exit the loop if code executes successfully
                
        else:
            await cl.Message(
                content="Ok, I won't execute the code.",
            ).send()
            break  # Exit the loop if user chooses not to execute
    cl.user_session.set("chat_history", chat_history)
