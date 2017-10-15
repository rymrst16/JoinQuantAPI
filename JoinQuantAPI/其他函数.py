'''
    定时运行，调用这些函数后, handle_data可以不实现
    注意：
    参数 func 必须是一个全局的函数, 不能是类的成员函数
    当 time 指定具体的几点几分时必须使用分钟级回测
    通过history/attribute_history取天数据时, 是不包括当天的数据的(即使在15:00和after_close里面也是如此),要取得当天数据,只能取分钟的
    这些函数可以重复调用。
    每次调用这些函数都会产生一个新的定时任务, 如果想修改或者删除旧的定时任务, 请先调用unschedule_all 来删除所有定时任务, 然后再添加新的.
    在一月/一周交易日数不够以致于monthday/weekday无法满足时,我们会找这周内最近的一个日期来执行
    run_monthly
    run_weekly
    run_daily
    参数
    func: 一个函数, 此函数必须接受一个参数, 就是 context
    monthday: 每月的第几个交易日, 可以是负数, 表示倒数第几个交易日
    weekday: 每周的第几个交易日, 可以是负数, 表示倒数第几个交易日
    time: 日内执行时间,具体到分钟,一个字符串,可以是具体执行时间,比如“10:00”,或者 “every_bar”,“open”, “before_open” 和 “after_close”, 他们的含义是:
        every_bar: 在每一个 bar 结束后调用. 按天会在每天的开盘时调用一次，按分钟会在每天的每分钟运行
        open: 开盘的第一分钟(等同于”9:30”)
        before_open: 开盘前(等同于”9:20”,但是请不要使用直接使用此时间,后续可能会调整)
        after_close: 收盘后(半小时内运行).
        注：当time不等于open/before_open/after_close时, 必须使用分钟级回测
    reference_security: 时间的参照标的。如参照’000001.XSHG’，交易时间为9:30­15:00。如参
    照’IF1512.CCFX’，2016­01­01之后的交易时间为9:30­15:00，在此之前为9:15­15:15。    返回
        None
'''
##

# 按月运行
run_monthly(func, monthday, time='open', reference_security)
# 按周运行
run_weekly(func, weekday, time='open', reference_security)
# 每天内何时运行
run_daily(func, time='open',)

'''
    取消所有定时运行 
    参数
        无
    返回
        None
'''
##
# 取消所有定时运行
unschedule_all()

'''
    会帮您在图表上画出收益曲线和基准的收益曲线，您也可以调用record函数来描画额外的曲线。因为我们是按天展现的，如果您使用按分钟回测，我们画出的点是您最后一次调用record的值。
    参数
        很多key=>value形式的参数，key曲线名称，value为值
    返回
        None
'''
##
record(**kwargs)

'''
    给用户自己发送消息, 暂时只支持微信消息
    注意
        要使用功能, 必须开启模拟交易的 微信通知.
        此功能只能在 模拟交易 中使用, 回测中使用会直接忽略, 无任何提示.
        微信消息每人每天不超过 5 条, 超出会失败.
        微信消息主页只显示前 200 个字符, 点击详情可查看全部消息,全部消息不得超过 10000 个字符
    参数
        message: 消息内容. 字符串.
        channel: 消息渠道, 暂时只支持微信: weixin. 默认值是 weixin    
    返回
        True/False, 表示是否发送成功. 当发送失败时, 会在日志中显示错误信息
'''
##
send_message(message, channel='weixin')

'''
    日志log
    分级别打log,跟python的logging模块一致,print输出的结果等同于log.info,但是print后面的每一个元素会占用一行
    参数
        参数可以是字符串、对象等 
    返回
        None
'''
##
log.error(content)
log.warn(content)
log.info(content)
log.debug(content)
print(content1, content2, ...)

'''
    write_file ­ 写文件
    写入内容到研究模块path文件, 写入后, 您可以立即在研究模块中看到这个文件
    参数
        path: 相对路径, 相对于您的私有空间的根目录的路径
        content: 文件内容,str或者unicode,如果是unicode,则会使用UTF­8编码再存储.可以是二进制内容.
        append: 是否是追加模式, 当为False会清除原有文件内容，默认为False.
    返回
        None
        如果写入失败(一般是因为路径不合法), 会抛出异常
'''
##
write_file(path, content, append=False)

'''
    read_file ­ 读文件
    读取你的私有文件(您的私有文件可以在研究模块中看到)
    参数
        path: 相对路径, 相对于您的私有空间的根目录的路径
    返回
        返回文件的原始内容, 不做任何decode.
'''
##
read_file(path)

'''
自定义python库
您可以在把.py文件放在’研究’的根目录,然后在回测中就可以通过import的方式来引用此文件.
注意: 暂时只能import研究根目录下的.py文件, 还不能import子目录下的文件(比如通过 import a.b.c 来引用
a/b/c.py)
'''

'''
自定义python库
您可以在把.py文件放在’研究’的根目录,然后在回测中就可以通过import的方式来引用此文件.
注意: 暂时只能import研究根目录下的.py文件, 还不能import子目录下的文件(比如通过 import a.b.c 来引用
a/b/c.py)
'''

'''
    股票代码格式转换
    将其他形式的股票代码转换为聚宽可用的股票代码形式。
    仅适用于A股市场股票代码以及基金代码
    示例：
    #输入
    for code in ('000001', 'SZ000001', '000001SZ', '000001.sz', '000001.XSHE'):
    print normalize_code(code)
    #输出
    000001.XSHE
    000001.XSHE
    000001.XSHE
    000001.XSHE
    000001.XSHE
'''
##
normalize_code()

