from aiogram import types, Dispatcher


class CustomBotCommands:
    DEFAULT = [
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("help", "Вывести справку"),
        types.BotCommand("register", "Зарегестрировать новое устройство для vpn"),
        types.BotCommand("show_my_keys", "Показать все зарегестрированные устройства"),
        types.BotCommand("delete_vpn_key", "Удалить устройство vpn"),
    ]
    ADMINS = [
        types.BotCommand("get_queued_users", "Получить всех в очереди"),
        types.BotCommand("approve_users", "Выслать подтверждение"),
        types.BotCommand("delete_users", "Силой удалить юзера"),
    ]


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(CustomBotCommands.DEFAULT)
