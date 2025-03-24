from aiogram import F, Router, Bot
from aiogram.filters.command import CommandStart
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.keyboards import *
from app.function import *

from config import TG_TOKEN

router = Router()
bot = Bot(token=TG_TOKEN)


class Reg(StatesGroup):
    menu_message_id = State()
    date_unload = State()
    odo_unload = State()
    addr_unload = State()
    luw_unload = State()
    awning_unload = State()
    date_zeroing = State()
    odo_zeroing = State()
    date_fuel = State()
    fuel = State()
    brand_fuel = State()
    date_plain_repair = State()
    plain_repair = State()
    date_note = State()
    text_note = State()
    date_delete = State()
    text_info_mounth = State()
    text_day = State()
    text_detail_mounth = State()
    text_fuel_mounth = State()
    text_pr_1 = State()
    text_pr_2 = State()
    text_pr_all = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    text = f'<i>выберите действие:</i>'
    sent_message = await message.answer(text=text, parse_mode=ParseMode.HTML, reply_markup=start)
    await state.set_state(Reg.menu_message_id)
    await state.update_data(menu_message_id=sent_message.message_id)


async def restart_start(chat_id: int, state: FSMContext):
    text = f'<i>выберите действие:</i>'
    sent_message = await bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML, reply_markup=start)
    await state.set_state(Reg.menu_message_id)
    await state.update_data(menu_message_id=sent_message.message_id)


async def restart_write(chat_id: int, state: FSMContext):
    text = f'<i>выберите действие:</i>'
    sent_message = await bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML, reply_markup=record)
    await state.set_state(Reg.menu_message_id)
    await state.update_data(menu_message_id=sent_message.message_id)


async def restart_read(chat_id: int, state: FSMContext):
    text = f'<i>выберите действие:</i>'
    sent_message = await bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML, reply_markup=play)
    await state.set_state(Reg.menu_message_id)
    await state.update_data(menu_message_id=sent_message.message_id)


@router.callback_query(F.data == 'back')
async def back(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    menu_message_id = data.get('menu_message_id')
    if menu_message_id:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=menu_message_id)
    await restart_start(callback.message.chat.id, state)


@router.callback_query(F.data == 'back_play')
async def back_play(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    menu_message_id = data.get('menu_message_id')
    if menu_message_id:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=menu_message_id)
    text = f'<i>выберите действие:</i>'
    sent_message = await callback.message.answer(text=text, parse_mode=ParseMode.HTML, reply_markup=play)
    await state.update_data(menu_message_id=sent_message.message_id)
    await callback.answer()


@router.callback_query(F.data == 'write')
async def write(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    menu_message_id = data.get('menu_message_id')
    if menu_message_id:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=menu_message_id)
    text = f'<i>выберите действие:</i>'
    sent_message = await callback.message.answer(text=text, parse_mode=ParseMode.HTML, reply_markup=record)
    await state.update_data(menu_message_id=sent_message.message_id)
    await callback.answer()


@router.callback_query(F.data == 'unload')
async def unload(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    menu_message_id = data.get('menu_message_id')
    if menu_message_id:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=menu_message_id)
    await state.set_state(Reg.date_unload)
    await callback.message.answer('Введите дату(дд.мм.гг)')


@router.message(Reg.date_unload)
async def date_unload(message: Message, state: FSMContext):
    try:
        if check_date(message.text):
            await state.update_data(date_unload=message.text)
            await state.set_state(Reg.odo_unload)
            await message.answer('Введите пробег на последней выгрузке')
    except:
        await state.clear()
        await message.answer(text='Неверная дата!', parse_mode=ParseMode.HTML)
        await restart_write(message.chat.id, state)


@router.message(Reg.odo_unload)
async def odo(message: Message, state: FSMContext):
    try:
        if check_odo(message.text):
            await state.update_data(odo_unload=message.text)
            await state.set_state(Reg.addr_unload)
            await message.answer('Введите адрес')
    except:
        await state.clear()
        await message.answer(text='Неверный формат пробега!', parse_mode=ParseMode.HTML)
        await restart_write(message.chat.id, state)


@router.message(Reg.addr_unload)
async def addr(message: Message, state: FSMContext):
    await state.update_data(addr_unload=message.text)
    await state.set_state(Reg.luw_unload)
    await message.answer('Кол-во ПРР')


@router.message(Reg.luw_unload)
async def luw(message: Message, state: FSMContext):
    try:
        if check_luw(message.text):
            await state.update_data(luw_unload=message.text)
            await state.set_state(Reg.awning_unload)
            await message.answer('Растентовка(д/н)')
    except:
        await state.clear()
        await message.answer(text='Не верный формат!', parse_mode=ParseMode.HTML)
        await restart_write(message.chat.id, state)


@router.message(Reg.awning_unload)
async def awning(message: Message, state: FSMContext):
    try:
        if check_awning(message.text):
            await state.update_data(awning_unload=message.text)
            data = await state.get_data()
            record_unload(data['date_unload'], data['odo_unload'], data['addr_unload'], data['luw_unload'], data['awning_unload'].lower())
            await message.answer('Запись добавлена')
            await state.clear()
            await restart_start(message.chat.id, state)
    except:
        await state.clear()
        await message.answer(text='Не верный формат, нужно "д" или "н"!', parse_mode=ParseMode.HTML)
        await restart_write(message.chat.id, state)


@router.callback_query(F.data == 'zeroing')
async def zeroing(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    menu_message_id = data.get('menu_message_id')
    if menu_message_id:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=menu_message_id)
    await state.set_state(Reg.date_zeroing)
    await callback.message.answer('Введите дату при обнулении')


@router.message(Reg.date_zeroing)
async def date_zeroing(message: Message, state: FSMContext):
    try:
        if check_date(message.text):
            await state.update_data(date_zeroing=message.text)
            await state.set_state(Reg.odo_zeroing)
            await message.answer('Введите пробег')
    except:
        await state.clear()
        await message.answer(text='Неверная дата!', parse_mode=ParseMode.HTML)
        await restart_write(message.chat.id, state)


@router.message(Reg.odo_zeroing)
async def odo_zeroing(message: Message, state: FSMContext):
    try:
        if check_odo(message.text):
            await state.update_data(odo_zeroing=message.text)
            data = await state.get_data()
            record_zeroing(data['date_zeroing'], data['odo_zeroing'])
            await message.answer('Запись добавлена')
            await state.clear()
            await restart_start(message.chat.id, state)
    except:
        await state.clear()
        await message.answer(text='Неверный формат пробега!', parse_mode=ParseMode.HTML)
        await restart_write(message.chat.id, state)


@router.callback_query(F.data == 'fuel')
async def fuel(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    menu_message_id = data.get('menu_message_id')
    if menu_message_id:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=menu_message_id)
    await state.set_state(Reg.date_fuel)
    await callback.message.answer('Введите дату')


@router.message(Reg.date_fuel)
async def date_fuel(message: Message, state: FSMContext):
    try:
        if check_date(message.text):   
            await state.update_data(date_fuel=message.text)
            await state.set_state(Reg.fuel)
            await message.answer('Введите объем топлива')
    except:
        await state.clear()
        await message.answer(text='Неверная дата!', parse_mode=ParseMode.HTML)
        await restart_write(message.chat.id, state)



@router.message(Reg.fuel)
async def fuel(message: Message, state: FSMContext):
    try:
        if check_fuel(message.text):
            await state.update_data(fuel=message.text)
            await state.set_state(Reg.brand_fuel)
            await message.answer('Введите бренд АЗС')
    except:
        await state.clear()
        await message.answer(text='Неверный формат объема!', parse_mode=ParseMode.HTML)
        await restart_write(message.chat.id, state)


@router.message(Reg.brand_fuel)
async def brand_fuel(message: Message, state: FSMContext):
    await state.update_data(brand_fuel=message.text)
    data = await state.get_data()
    record_fuel(data['date_fuel'], data['fuel'], data['brand_fuel'])
    await message.answer('Запись добавлена')
    await state.clear()
    await restart_start(message.chat.id, state)


@router.callback_query(F.data == 'plain_repair')
async def plain_repair(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    menu_message_id = data.get('menu_message_id')
    if menu_message_id:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=menu_message_id)
    await state.set_state(Reg.date_plain_repair)
    await callback.message.answer('Введите дату')


@router.message(Reg.date_plain_repair)
async def date_plain_repair(message: Message, state: FSMContext):
    try:
        if check_date(message.text):        
            await state.update_data(date_plain_repair=message.text)
            await state.set_state(Reg.plain_repair)
            await message.answer('Простой/ремонт(п/р) ?')
    except:
        await state.clear()
        await message.answer(text='Неверная дата!', parse_mode=ParseMode.HTML)
        await restart_write(message.chat.id, state)


@router.message(Reg.plain_repair)
async def plain_repair(message: Message, state: FSMContext):
    try:
        if check_plain_repair(message.text):         
            await state.update_data(plain_repair=message.text)
            data = await state.get_data()
            record_plain_repair(data['date_plain_repair'], data['plain_repair'])
            await message.answer('Запись добавлена')
            await state.clear()
            await restart_start(message.chat.id, state)
    except:
        await state.clear()
        await message.answer(text='Неверный формат, нужно "п" или "р"!', parse_mode=ParseMode.HTML)
        await restart_write(message.chat.id, state)


@router.callback_query(F.data == 'note')
async def note(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    menu_message_id = data.get('menu_message_id')
    if menu_message_id:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=menu_message_id)
    await state.set_state(Reg.date_note)
    await callback.message.answer('Введите дату')


@router.message(Reg.date_note)
async def date_note(message: Message, state: FSMContext):
    try:
        if check_date(message.text):
            await state.update_data(date_note=message.text)
            await state.set_state(Reg.text_note)
            await message.answer('Введите комментарий')
    except:
        await state.clear()
        await message.answer(text='Неверная дата!', parse_mode=ParseMode.HTML)
        await restart_write(message.chat.id, state)


@router.message(Reg.text_note)
async def text_note(message: Message, state: FSMContext):
    await state.update_data(text_note=message.text)
    data = await state.get_data()
    record_note(data['date_note'], data['text_note'])
    await message.answer('Комментарий добавлен')
    await state.clear()
    await restart_start(message.chat.id, state)


@router.callback_query(F.data == 'delete_date')
async def delete_date(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    menu_message_id = data.get('menu_message_id')
    if menu_message_id:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=menu_message_id)
    await state.set_state(Reg.date_delete)
    await callback.message.answer('Введите дату')


@router.message(Reg.date_delete)
async def date_delete(message: Message, state: FSMContext):
    try:
        if check_date(message.text):
            try:
                await state.update_data(date_delete=message.text)
                data = await state.get_data()
                delete_to_date(data['date_delete'])
                await message.answer('Запись удалена')
                await state.clear()
                await restart_start(message.chat.id, state)
            except:
                await state.clear()
                await message.answer(text='Нет такой даты!', parse_mode=ParseMode.HTML)
                await restart_write()(message.chat.id, state)
    except:
        await state.clear()
        await message.answer(text='Неверная дата!', parse_mode=ParseMode.HTML)
        await restart_write(message.chat.id, state)


@router.callback_query(F.data == 'read')
async def read(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    menu_message_id = data.get('menu_message_id')
    if menu_message_id:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=menu_message_id)
    text = f'<i>выберите действие:</i>'
    sent_message = await callback.message.answer(text=text, parse_mode=ParseMode.HTML, reply_markup=play)
    await state.update_data(menu_message_id=sent_message.message_id)
    await callback.answer()


@router.callback_query(F.data == 'info_mounth')
async def info_mounth(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    menu_message_id = data.get('menu_message_id')
    if menu_message_id:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=menu_message_id)
    await state.set_state(Reg.text_info_mounth)
    await callback.message.answer('Введите месяц(мм.гг)')


@router.message(Reg.text_info_mounth)
async def mounth(message: Message, state: FSMContext):
    try:
        if check_mounth(message.text):
            await state.update_data(text_info_mounth=message.text)
            data = await state.get_data()
            mm = data['text_info_mounth'].split('.')[0]
            gg = data['text_info_mounth'].split('.')[1]
            try:
                res = str(info_for_mounth(int(mm), int(gg)))
                await message.answer(res, parse_mode=ParseMode.HTML)
                await state.clear()
                await restart_start(message.chat.id, state)
            except:
                await state.clear()
                await message.answer(text='Нет данных!', parse_mode=ParseMode.HTML)
                await restart_read(message.chat.id, state)
    except:
        await state.clear()
        await message.answer(text='Неверный формат месяца, нужно "мм.гг"!', parse_mode=ParseMode.HTML)
        await restart_read(message.chat.id, state)


@router.callback_query(F.data == 'info_day')
async def info_day(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    menu_message_id = data.get('menu_message_id')
    if menu_message_id:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=menu_message_id)
    await state.set_state(Reg.text_day)
    await callback.message.answer('Введите день(дд.мм.гг)')


@router.message(Reg.text_day)
async def fun_day(message: Message, state: FSMContext):
    try:
        if check_date(message.text):        
            await state.update_data(text_day=message.text)
            data = await state.get_data()
            res = str(day(data['text_day']))
            await message.answer(res, parse_mode=ParseMode.HTML)
            await state.clear()
            await restart_read(message.chat.id, state)
    except:
        await state.clear()
        await message.answer(text='Неверная дата!', parse_mode=ParseMode.HTML)
        await restart_read(message.chat.id, state)


@router.callback_query(F.data == 'detail_mounth')
async def detail_mounth(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    menu_message_id = data.get('menu_message_id')
    if menu_message_id:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=menu_message_id)
    await state.set_state(Reg.text_detail_mounth)
    await callback.message.answer('Введите месяц(мм.гг)')


@router.message(Reg.text_detail_mounth)
async def fun_detail_mounth(message: Message, state: FSMContext):
    try:
        if check_mounth(message.text):
            try:      
                await state.update_data(text_detail_mounth=message.text)
                data = await state.get_data()
                mm = data['text_detail_mounth'].split('.')[0]
                gg = data['text_detail_mounth'].split('.')[1]
                res = detail_for_mounth(int(mm), int(gg))
                for i in res:
                    await message.answer(i, parse_mode=ParseMode.HTML)
                await state.clear()
                await restart_read(message.chat.id, state)
            except:
                await state.clear()
                await message.answer(text='Нет данных!', parse_mode=ParseMode.HTML)
                await restart_read(message.chat.id, state)
    except:
        await state.clear()
        await message.answer(text='Неверный формат месяца, нужно "мм.гг"!', parse_mode=ParseMode.HTML)
        await restart_read(message.chat.id, state)


@router.callback_query(F.data == 'fuel_mounth')
async def fuel_mounth(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    menu_message_id = data.get('menu_message_id')
    if menu_message_id:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=menu_message_id)
    await state.set_state(Reg.text_fuel_mounth)
    await callback.message.answer('Введите месяц(мм.гг)')


@router.message(Reg.text_fuel_mounth)
async def fun_fuel_mounth(message: Message, state: FSMContext):
    try:
        if check_mounth(message.text):
            try:
                await state.update_data(text_fuel_mounth=message.text)
                data = await state.get_data()
                mm = data['text_fuel_mounth'].split('.')[0]
                gg = data['text_fuel_mounth'].split('.')[1]
                res = fuel_for_mounth(int(mm), int(gg))
                await message.answer(res, parse_mode=ParseMode.HTML)
                await state.clear()
                await restart_start(message.chat.id, state)
            except:
                await state.clear()
                await message.answer(text='Нет данных!', parse_mode=ParseMode.HTML)
                await restart_read(message.chat.id, state)
    except:
        await state.clear()
        await message.answer(text='Неверный формат месяца, нужно "мм.гг"!', parse_mode=ParseMode.HTML)
        await restart_read(message.chat.id, state)


@router.callback_query(F.data == 'pr')
async def pr(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    menu_message_id = data.get('menu_message_id')
    if menu_message_id:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=menu_message_id)
    text = f'<i>выберите действие:</i>'
    sent_message = await callback.message.answer(text=text, parse_mode=ParseMode.HTML, reply_markup=play_pr)
    await state.update_data(menu_message_id=sent_message.message_id)
    await callback.answer()


@router.callback_query(F.data == 'pr_1')
async def pr_1(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    menu_message_id = data.get('menu_message_id')
    if menu_message_id:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=menu_message_id)
    await state.set_state(Reg.text_pr_1)
    await callback.message.answer('Введите месяц(мм.гг)')


@router.message(Reg.text_pr_1)
async def fun_pr_1(message: Message, state: FSMContext):
    try:
        if check_mounth(message.text):
            try:
                await state.update_data(text_pr_1=message.text)
                data = await state.get_data()
                mm = data['text_pr_1'].split('.')[0]
                gg = data['text_pr_1'].split('.')[1]
                res = plain_repair15_15(int(mm), int(gg), 'one')
                await message.answer(res, parse_mode=ParseMode.HTML)
                await state.clear()
                await restart_start(message.chat.id, state)
            except:
                await state.clear()
                await message.answer(text='Нет данных!', parse_mode=ParseMode.HTML)
                await restart_read(message.chat.id, state)
    except:
        await state.clear()
        await message.answer(text='Неверный формат месяца, нужно "мм.гг"!', parse_mode=ParseMode.HTML)
        await restart_read(message.chat.id, state)


@router.callback_query(F.data == 'pr_2')
async def pr_2(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    menu_message_id = data.get('menu_message_id')
    if menu_message_id:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=menu_message_id)
    await state.set_state(Reg.text_pr_2)
    await callback.message.answer('Введите месяц(мм.гг)')


@router.message(Reg.text_pr_2)
async def fun_pr_2(message: Message, state: FSMContext):
    try:
        if check_mounth(message.text):
            try:
                await state.update_data(text_pr_2=message.text)
                data = await state.get_data()
                mm = data['text_pr_2'].split('.')[0]
                gg = data['text_pr_2'].split('.')[1]
                res = plain_repair15_15(int(mm), int(gg), 'two')
                await message.answer(res, parse_mode=ParseMode.HTML)
                await state.clear()
                await restart_start(message.chat.id, state)
            except:
                await state.clear()
                await message.answer(text='Нет данных!', parse_mode=ParseMode.HTML)
                await restart_read(message.chat.id, state)
    except:
        await state.clear()
        await message.answer(text='Неверный формат месяца, нужно "мм.гг"!', parse_mode=ParseMode.HTML)
        await restart_read(message.chat.id, state)



@router.callback_query(F.data == 'pr_all')
async def pr_all(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    menu_message_id = data.get('menu_message_id')
    if menu_message_id:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=menu_message_id)
    await state.set_state(Reg.text_pr_all)
    await callback.message.answer('Введите месяц(мм.гг)')


@router.message(Reg.text_pr_all)
async def fun_pr_all(message: Message, state: FSMContext):
    try:
        if check_mounth(message.text):
            try:
                await state.update_data(text_pr_all=message.text)
                data = await state.get_data()
                mm = data['text_pr_all'].split('.')[0]
                gg = data['text_pr_all'].split('.')[1]
                res = plain_repair15_15(int(mm), int(gg))
                await message.answer(res, parse_mode=ParseMode.HTML)
                await state.clear()
                await restart_start(message.chat.id, state)
            except:
                await state.clear()
                await message.answer(text='Нет данных!', parse_mode=ParseMode.HTML)
                await restart_read(message.chat.id, state)

    except:
        await state.clear()
        await message.answer(text='Неверный формат месяца, нужно "мм.гг"!', parse_mode=ParseMode.HTML)
        await restart_read(message.chat.id, state)
