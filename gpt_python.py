import openai
import os
import time


def create_chat(chat_array):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=chat_array,
        temperature=0.8,
        frequency_penalty=0,
        presence_penalty=0.6,
    )
    return response


def verify() -> str:  
    key='sk-XXXXXXXXX'
    return key


def create_record_filename():
    time_tuple = time.localtime(time.time())
    # current_year = str(time_tuple[0])
    current_month = str(time_tuple[1])
    current_day = str(time_tuple[2]).zfill(2)
    current_hour = str(time_tuple[3]).zfill(2)
    current_minute = str(time_tuple[4]).zfill(2)
    current_second = str(time_tuple[5]).zfill(2)
    filename = '{}月{}日-{}时{}分{}秒.txt'.format(current_month, current_day, current_hour, current_minute,
                                                  current_second)
    return filename


def record_text(new_message, response_message, filename):
    if not (os.path.isdir('./record')):
        os.mkdir('./record')
    out = '{}: {}\n{}: {}\n'.format(new_message['role'], new_message['content'], response_message['role'],
                                    response_message['content'])
    with open('./record/{}'.format(filename), 'a', encoding='utf-8') as F:
        F.write(out)


if __name__ == '__main__':
    openai.api_key = verify()
    mode_setting = '万能的什么都会的俏皮的gpt3.5_turbo'
    messages = [
        {'role': 'system', 'content': mode_setting},
    ]
    filename = create_record_filename()
    print("连接成功，开启对话：")
    while (True):
        human_input = input('你: ')
        new_message = {
            'role': 'user',
            'content': human_input
        }
        messages.append(new_message)
        response = create_chat(chat_array=messages)
        response_message = response['choices'][0]['message']
        messages.append(response_message)
        print('{}: {}'.format('gpt_turbo', response_message['content']))
        record_text(new_message, response_message, filename)
