from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import link
import json
from os.path import isfile
from re import sub

bot = Bot(token='7683497463:AAF2vxBAkM0zNpya3dUEUqx_EFo6-GHswSw')
dp = Dispatcher(bot)
channels = [-1002065937026, -1002233290926]  # Список каналов для подписки
admins = [505655010, 958883427]

# Укажите ID победителя здесь
winner_id = "5870409794"  # Замените на ID реального победителя

# Проверка существования файла и загрузка участников
def load_participants():
    if isfile('participants.malw'):
        with open('participants.malw', 'r') as file:
            return json.loads(file.read())
    else:
        return []

def save_participants(participants):
    with open('participants.malw', 'w') as file:
        file.write(json.dumps(participants))

participants = load_participants()


@dp.message_handler(commands='start')
async def start(message: types.Message):
    global participants, channels
    user_id = str(message['from']['id'])

    if user_id in participants:
        await message.reply('*🎉 Ты уже участвуешь в розыгрыше!*\nНе переживай, результаты не за горами 😎🎮', parse_mode='markdown', disable_web_page_preview=True)
        return

    not_subscribed_channels = []
    for channel in channels:
        try:
            user_info = await bot.get_chat_member(channel, message['from']['id'])
            if user_info['status'] not in ['member', 'creator', 'administrator']:
                raise
        except Exception as e:
            channel_info = await bot.get_chat(channel)
            not_subscribed_channels.append(link(channel_info['title'], 'https://t.me/' + channel_info['username']))
    
    if not_subscribed_channels:
        message_text = "❌ Ты не подписан на следующие каналы:\n" + "\n".join(not_subscribed_channels)
        await message.reply(message_text + "\nЧтобы участвовать в розыгрыше ты *обязан* быть подписан на *оба* канала🤞.\nПосле подписки отправь мне */start*", parse_mode='markdown', disable_web_page_preview=True)
        return

    participants.append(user_id)
    save_participants(participants)
    await message.reply('🎉 Ты успешно стал участником розыгрыша! *Желаем удачи🍀*', parse_mode='markdown', disable_web_page_preview=True)

@dp.message_handler(commands='check')
async def check(message: types.Message):
    global participants, channels
    if message['from']['id'] in admins:
        for participant in participants:
            for channel in channels:
                try:
                    user_info = await bot.get_chat_member(channel, participant)
                    if user_info['status'] not in ['member', 'creator', 'administrator']:
                        raise
                except Exception as e:
                    channel_info = await bot.get_chat(channel)
                    try:
                        await bot.send_message(
                            participant,
                            '⚠️ Ты вышел из канала ' + link(channel_info['title'], 'https://t.me/' + channel_info['username']) +
                            ', поэтому больше не участвуешь в розыгрыше 😔',
                            parse_mode='markdown', disable_web_page_preview=True
                        )
                    except:
                        pass
                    participants.remove(participant)
                    break
        save_participants(participants)
        await message.reply('✅ Проверка завершена! Все участники обновлены.', disable_web_page_preview=True)

@dp.message_handler(commands='end')
async def end(message: types.Message):
    if message['from']['id'] in admins:
        winner_name = await bot.get_chat(winner_id)
        for ts in sub('[A-Za-zА-Яа-я0-9 ]', '', winner_name['first_name']):
            winner_name['first_name'] = winner_name['first_name'].replace(ts, '')
        if winner_name['first_name'].replace(' ', '') == '':
            winner_name['first_name'] = 'Пустой или засранный ник'
        if 'username' in winner_name:
            name = link(winner_name['first_name'], 'https://t.me/' + winner_name['username']) + '\n'
        elif not "has_private_forwards" in winner_name:
            name = link(winner_name['first_name'], 'tg://user?id=' + winner_id) + '\n'
        else:
            name = winner_name['first_name'] + ' (невозможно упомянуть)' + '\n'
        for participant in participants:
            try:
                await bot.send_message(participant, 
                    f'*🎉 Масштабный розыгрыш подошел к концу! 🥳*\nСистема выбрала победителя:\nПобедитель — {name}\n\nСледите за [R&M STORE](https://t.me/romangame36), [XTATi | MUSIC 🎵](https://t.me/xtatimusic) и ждите новые *розыгрыши с крутыми призами! 🕹️*',
                    parse_mode='Markdown', disable_web_page_preview=True)
            except Exception as e:
                print(f"Не удалось отправить сообщение участнику {participant}: {e}")
        
        await message.reply('✅ Сообщение о победителе было отправлено всем участникам!', disable_web_page_preview=True)
            
       

@dp.message_handler(commands='testend')
async def testend(message: types.Message):
    if message['from']['id'] in admins:
        winner_name = await bot.get_chat(winner_id)
        for ts in sub('[A-Za-zА-Яа-я0-9 ]', '', winner_name['first_name']):
            winner_name['first_name'] = winner_name['first_name'].replace(ts, '')
        if winner_name['first_name'].replace(' ', '') == '':
            winner_name['first_name'] = 'Пустой или засранный ник'
        if 'username' in winner_name:
            name = link(winner_name['first_name'], 'https://t.me/' + winner_name['username']) + '\n'
        elif not "has_private_forwards" in winner_name:
            name = link(winner_name['first_name'], 'tg://user?id=' + winner_id) + '\n'
        else:
            name = winner_name['first_name'] + ' (невозможно упомянуть)' + '\n'
        await message.reply('*🎉 Масштабный розыгрыш подошел к концу! 🥳*\nСистема выбрала победителя:\nПобедитель — ' + name +'\n\nСледите за [R&M STORE](https://t.me/romangame36), [XTATi | MUSIC 🎵](https://t.me/xtatimusic) и ждите новые *розыгрыши с крутыми призами! 🕹️*', parse_mode='Markdown', disable_web_page_preview=True)
        
@dp.message_handler(commands='list')
async def list(message: types.Message):
    global participants
    if message['from']['id'] in admins:
        if participants == []:
            await message.reply('🚫 В розыгрыше ещё никто не участвует! 🤷‍', disable_web_page_preview=True)
            return
        list_output = '📜 Список участников розыгрыша:\n'
        for participant in participants:
            participant_info = await bot.get_chat(participant)
            for ts in sub('[A-Za-zА-Яа-я0-9 ]', '', participant_info['first_name']):
                participant_info['first_name'] = participant_info['first_name'].replace(ts, '')
            if participant_info['first_name'].replace(' ', '') == '':
                participant_info['first_name'] = 'Пустой или засранный ник'
            if 'username' in participant_info:
                list_output += link(participant_info['first_name'], 'https://t.me/' + participant_info['username']) + '\n'
            elif not "has_private_forwards" in participant_info:
                list_output += link(participant_info['first_name'], 'tg://user?id=' + participant) + '\n'
            else:
                list_output += participant_info['first_name'] + ' (невозможно упомянуть)' + '\n'
        await message.reply(list_output, parse_mode='markdown', disable_web_page_preview=True)

executor.start_polling(dp, skip_updates=True)
