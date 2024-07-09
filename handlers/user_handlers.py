import asyncio

import aiohttp
from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from lexicon.lexicon import LEXICON
from models.base import Session, Users, Friends
from FSM.fsm import FSMFillForm
from aiogram.fsm.state import default_state
import requests

router = Router()
session = Session()


@router.message(CommandStart(), StateFilter(default_state))
async def welcome(message: Message):
    await message.answer(LEXICON[message.text])

    if session.query(Users).filter(Users.user_id == message.from_user.id).first() is not None:
        await message.answer(
            text=LEXICON['fillform']
        )
    else:
        #
        await message.answer(text=LEXICON['/help'])


@router.message(Command(commands='help'), StateFilter(default_state))
async def help(message: Message):
    await message.answer(LEXICON[message.text])


@router.message(Command(commands='fillform'), StateFilter(default_state))
async def fillform(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['enter_friend_username'])
    await state.set_state(FSMFillForm.fill_name)


@router.message(Command(commands='cancel'), StateFilter(default_state))
async def cancel(message: Message):
    await message.answer(text=LEXICON['cancel_no_state'])


@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel(message: Message, state: FSMContext):
    await message.answer(
        text=LEXICON['cancel_in_state']
    )
    await state.clear()


@router.message(StateFilter(FSMFillForm.fill_name))
async def fill_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    nick = await state.get_data()
    url = f"https://leetcode-api-faisalshohag.vercel.app/{nick['name']}"
    response = requests.get(url)
    if 'errors' in response.json():
        await message.answer(text=LEXICON['invalid_username'])
    else:

        new_user = Users(user_id=message.from_user.id, login=nick)
        session.add(new_user)
        session.commit()
        await message.answer(text=LEXICON['/help'])
        await state.clear()


@router.message(Command(commands='contestrank'), StateFilter(default_state))
async def rankByContest(message: Message):
    id = message.from_user.id
    user = session.query(Users).filter(Users.user_id == id).first()
    login = user.login
    lst = [[0, login]]
    friends = session.query(Friends).filter(Friends.id == id).all()
    for i in friends:
        lst.append([0, i.user_name, 0, 0, 0])

    async def fetch_total_solved(sessions, username):
        url = "https://leetcode.com/graphql"
        query = """
                   {
                       userContestRanking(username:  "%s")  {
                            rating
                        }
                   }
                   """ % username
        async with sessions.post(url, json={'query': query}) as response:
            data = await response.json()
            if data['data']['userContestRanking'] is None:
                return 0
            return data['data']['userContestRanking']['rating']

    async with aiohttp.ClientSession() as sessions:
        tasks = [fetch_total_solved(sessions, user[1]) for user in lst]
        results = await asyncio.gather(*tasks)
        for i, totalSolved in enumerate(results):
            lst[i][0] = totalSolved

    lst.sort(reverse=True)
    ans = '```\n'
    ans += f"{'№':<3} | {'Имя':<15} | {'totalSolved':<15}\n"
    ans += '-' * 30 + '\n'

    for j in range(len(lst)):
        formatted_number = round(lst[j][0])

        formatted_row = f"{j + 1:<3} | {lst[j][1]:<15} | {formatted_number}"
        ans += formatted_row + '\n'

    ans += '```'  # Конец блока моноширинного текста
    await message.answer(text=ans, parse_mode='MarkdownV2')


@router.message(Command(commands='totalrank'), StateFilter(default_state))
async def rankByContest(message: Message):
    id = message.from_user.id
    user = session.query(Users).filter(Users.user_id == id).first()
    login = user.login
    lst = [[0, login]]
    friends = session.query(Friends).filter(Friends.id == id).all()
    for i in friends:
        lst.append([0, i.user_name, 0, 0, 0])

    async def fetch_total_solved(sessions, username):
        url = "https://leetcode.com/graphql"
        query = """
           {
             matchedUser(username: "%s") {
               username
               submitStats: submitStatsGlobal {
                 acSubmissionNum {
                   count
                 }
               }
             }
           }
           """ % username
        async with sessions.post(url, json={'query': query}) as response:
            data = await response.json()
            return data['data']['matchedUser']['submitStats']['acSubmissionNum'][0]['count']

    async with aiohttp.ClientSession() as sessions:
        task = [fetch_total_solved(sessions, user[1]) for user in lst]
        result = await asyncio.gather(*task)
        for i, totalSolved in enumerate(result):
            lst[i][0] = totalSolved

    lst.sort(reverse=True)
    ans = '```\n'
    ans += f"{'№':<3} | {'Имя':<15} | {'totalSolved':<15}\n"
    ans += '-' * 30 + '\n'

    for j in range(len(lst)):
        formatted_number = round(lst[j][0])

        formatted_row = f"{j + 1:<3} | {lst[j][1]:<15} | {formatted_number}"
        ans += formatted_row + '\n'

    ans += '```'
    await message.answer(text=ans, parse_mode='MarkdownV2')


@router.message(Command(commands='easyrank'), StateFilter(default_state))
async def rankByContest(message: Message):
    id = message.from_user.id
    user = session.query(Users).filter(Users.user_id == id).first()
    login = user.login
    lst = [[0, login]]
    friends = session.query(Friends).filter(Friends.id == id).all()
    for i in friends:
        lst.append([0, i.user_name, 0, 0, 0])

    async def fetch_total_solved(sessions, username):
        url = "https://leetcode.com/graphql"
        query = """
              {
                matchedUser(username: "%s") {
                  username
                  submitStats: submitStatsGlobal {
                    acSubmissionNum {
                      count
                    }
                  }
                }
              }
              """ % username
        async with sessions.post(url, json={'query': query}) as response:
            data = await response.json()
            return data['data']['matchedUser']['submitStats']['acSubmissionNum'][1]['count']

    async with aiohttp.ClientSession() as sessions:
        task = [fetch_total_solved(sessions, user[1]) for user in lst]
        result = await asyncio.gather(*task)
        for i, totalSolved in enumerate(result):
            lst[i][0] = totalSolved

    lst.sort(reverse=True)
    ans = '```\n'
    ans += f"{'№':<3} | {'Имя':<15} | {'easySolved':<15}\n"
    ans += '-' * 30 + '\n'

    for j in range(len(lst)):
        formatted_number = round(lst[j][0])

        formatted_row = f"{j + 1:<3} | {lst[j][1]:<15} | {formatted_number}"
        ans += formatted_row + '\n'

    ans += '```'
    await message.answer(text=ans, parse_mode='MarkdownV2')


@router.message(Command(commands='mediumrank'), StateFilter(default_state))
async def rankByContest(message: Message):
    id = message.from_user.id
    user = session.query(Users).filter(Users.user_id == id).first()
    login = user.login
    lst = [[0, login]]
    friends = session.query(Friends).filter(Friends.id == id).all()
    for i in friends:
        lst.append([0, i.user_name, 0, 0, 0])

    async def fetch_total_solved(sessions, username):
        url = "https://leetcode.com/graphql"
        query = """
              {
                matchedUser(username: "%s") {
                  username
                  submitStats: submitStatsGlobal {
                    acSubmissionNum {
                      count
                    }
                  }
                }
              }
              """ % username
        async with sessions.post(url, json={'query': query}) as response:
            data = await response.json()
            return data['data']['matchedUser']['submitStats']['acSubmissionNum'][2]['count']

    async with aiohttp.ClientSession() as sessions:
        task = [fetch_total_solved(sessions, user[1]) for user in lst]
        result = await asyncio.gather(*task)
        for i, totalSolved in enumerate(result):
            lst[i][0] = totalSolved

    lst.sort(reverse=True)
    ans = '```\n'
    ans += f"{'№':<3} | {'Имя':<15} | {'mediumSolved':<15}\n"
    ans += '-' * 30 + '\n'

    for j in range(len(lst)):
        formatted_number = round(lst[j][0])

        formatted_row = f"{j + 1:<3} | {lst[j][1]:<15} | {formatted_number}"
        ans += formatted_row + '\n'

    ans += '```'
    await message.answer(text=ans, parse_mode='MarkdownV2')


@router.message(Command(commands='hardrank'), StateFilter(default_state))
async def rankByContest(message: Message):
    id = message.from_user.id
    user = session.query(Users).filter(Users.user_id == id).first()
    login = user.login
    lst = [[0, login]]
    friends = session.query(Friends).filter(Friends.id == id).all()
    for i in friends:
        lst.append([0, i.user_name, 0, 0, 0])

    async def fetch_total_solved(sessions, username):
        url = "https://leetcode.com/graphql"
        query = """
              {
                matchedUser(username: "%s") {
                  username
                  submitStats: submitStatsGlobal {
                    acSubmissionNum {
                      count
                    }
                  }
                }
              }
              """ % username
        async with sessions.post(url, json={'query': query}) as response:
            data = await response.json()
            return data['data']['matchedUser']['submitStats']['acSubmissionNum'][3]['count']

    async with aiohttp.ClientSession() as sessions:
        task = [fetch_total_solved(sessions, user[1]) for user in lst]
        result = await asyncio.gather(*task)
        for i, totalSolved in enumerate(result):
            lst[i][0] = totalSolved

    lst.sort(reverse=True)
    ans = '```\n'
    ans += f"{'№':<3} | {'Имя':<15} | {'hardSolved':<15}\n"
    ans += '-' * 30 + '\n'

    for j in range(len(lst)):
        formatted_number = round(lst[j][0])

        formatted_row = f"{j + 1:<3} | {lst[j][1]:<15} | {formatted_number}"
        ans += formatted_row + '\n'

    ans += '```'
    await message.answer(text=ans, parse_mode='MarkdownV2')


@router.message(Command(commands='addfriends'), StateFilter(default_state))
async def addFriends(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['enter_friend_username'])
    await state.set_state(FSMFillForm.fill_friends)


@router.message(StateFilter(FSMFillForm.fill_friends))
async def fill_friends(message: Message, state: FSMContext):
    id = message.from_user.id
    await state.update_data(name=message.text)
    nick = await state.get_data()
    url = "https://leetcode.com/graphql"
    query = """
               {
                   userContestRanking(username:  "%s")  {
                        rating
                    }
               }
               """ % nick['name']
    response = requests.post(url, json={'query': query})
    if 'errors' in response.json():
        await message.answer(text=LEXICON['invalid_username'])
    else:
        user = Friends(user_name=nick['name'], id=id)
        session.add(user)
        session.commit()
        await message.answer(text=LEXICON['friend_added'])
        await state.clear()


@router.message(Command(commands='deletefriends'), StateFilter(default_state))
async def deleteFriends(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['fillform_prompt'])
    await state.set_state(FSMFillForm.delete_friends)


@router.message(StateFilter(FSMFillForm.delete_friends))
async def delete_friends(message: Message, state: FSMContext):
    id = message.from_user.id
    await state.update_data(name=message.text)
    nick = await state.get_data()
    session.query(Friends).filter(Friends.id == id, Friends.user_name == nick['name']).delete()
    session.commit()
    await message.answer(text=LEXICON['friend_deleted'])
    await state.clear()
