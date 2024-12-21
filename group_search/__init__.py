from nonebot import on_command
from nonebot.adapters.onebot.v11 import (
    Bot,
    Event,
    Message,
    MessageSegment
)
from nonebot.params import CommandArg
from .data_source import search
from .updater import *  # noqa: F403

search_gruop = on_command('fumo 搜索群组', priority=4, block=True)
@search_gruop.handle()
async def search_group_handler(bot: Bot, event: Event, args: Message = CommandArg()):
    keyword = args.extract_plain_text()
    if keyword:
        result = search(keyword)
        msg = MessageSegment.node_custom(user_id=111, nickname='你谁啊', content=f'>>> {keyword} 的结果如下:')
        for i in result:
            msg += MessageSegment.node_custom(user_id=111, nickname='你谁啊', content=i)
        await search_gruop.finish(msg)
    
    else:
        await search_gruop.finish('>>> 你还没有输入任何参数哦！随意输入看看会发生什么吧！')