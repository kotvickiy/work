from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Записать', callback_data='write')],
    [InlineKeyboardButton(text='Посмотреть', callback_data='read')]
])


record = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Выгрузка', callback_data='unload')],
    [InlineKeyboardButton(text='Обнуление', callback_data='zeroing')],
    [InlineKeyboardButton(text='Заправка', callback_data='fuel')],
    [InlineKeyboardButton(text='Простой/Ремонт', callback_data='plain_repair')],
    [InlineKeyboardButton(text='Примечание', callback_data='note')],
    [InlineKeyboardButton(text='Удаление записи', callback_data='delete_date')],
    [InlineKeyboardButton(text='Назад', callback_data='back')],
    ])


play = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Информация за месяц', callback_data='info_mounth')],
    [InlineKeyboardButton(text='Информация за день', callback_data='info_day')],
    [InlineKeyboardButton(text='Подробно за месяц', callback_data='detail_mounth')],
    [InlineKeyboardButton(text='Заправлено за месяц', callback_data='fuel_mounth')],
    [InlineKeyboardButton(text='Простои/Ремонты', callback_data='pr')],
    [InlineKeyboardButton(text='Назад', callback_data='back')]
])


play_pr = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='За первую половину', callback_data='pr_1')],
    [InlineKeyboardButton(text='За вторую половину', callback_data='pr_2')],
    [InlineKeyboardButton(text='За месяц', callback_data='pr_all')],
    [InlineKeyboardButton(text='Назад', callback_data='back_play')]

])
