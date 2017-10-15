'''
    order ­ 按股数下单
    买卖标的。调用成功后,您将可以调用get_open_orders取得所有未完成的交易,也可以调用cancel_order取消交易
    可能的失败原因:
        1. 股票数量经调整后变成0 (请看下面的说明)
        2. 股票停牌
        3. 股票未上市或者退市
        4. 股票不存在
        5. 为股票、基金开了空单
        6. 选择了不存在的仓位号，如没有建立多个仓位，而设定pindex的数大于0
        对于原因4, 我们会抛出异常停止运行, 因为我们认为这是您代码的bug.
        注意:
            因为下列原因, 有时候实际买入或者卖出的股票数量跟您设置的不一样，这个时候我们会在您的log中添加警告信息。
                1. 买入时会根据您当前的现金来限制您买入的数量
                2. 卖出时会根据您持有股票的数量来限制您卖出的数量
                3. 我们会遵守A股交易规则:每次交易数量只能是100的整数倍,但是卖光所有股票时不受这个限制
            根据交易所规则,每天结束时会取消所有未完成交易
    参数
        security: 标的代码
        amount: 交易数量, 正数表示买入, 负数表示卖出
        style: 参见order styles, None代表MarketOrder
        side: ‘long’/’short’，开空单还是多单。默认为多单，股票、基金暂不支持开空单。
        pindex: 在使用set_subportfolios创建了多个仓位时，指定subportfolio 的序号,从0开始,比如0指定第一个subportfolio,1指定第二个subportfolio，默认为0。
    返回
        Order对象或者None, 如果创建订单成功, 则返回Order对象, 失败则返回None
'''
##
order(security, amount, style=None, side='long', pindex=0)

'''
    order_target ­ 目标股数下单
    买卖标的, 使最终标的的数量达到指定的amount
    参数
        security: 标的代码
        amount: 期望的最终数量
        style: 参见order styles, None代表MarketOrder
        side: ‘long’/’short’，平空单还是多单。默认为多单，股票、基金暂不支持开空单。
        pindex:在使用set_subportfolios创建了多个仓位时，指定subportfolio的序号,从 0开始,比如0为指定第一个subportfolio,1为指定第二个subportfolio，默认为0。
    返回
        Order对象或者None, 如果创建委托成功, 则返回Order对象, 失败则返回None
'''
##
order(security, amount, style=None, side='long', pindex=0)

'''
    order_value ­ 按价值下单
    买卖价值为value的股票，金融期货暂不支持该API
    参数
        security: 股票名字
        value: 股票价值
        style: 参见order styles, None代表MarketOrder
        side: ‘long’/’short’，平空单还是多单。默认为多单，股票、基金暂不支持开空单。
        pindex: 在使用set_subportfolios创建了多个仓位时，指定subportfolio的序号,从0开始,比如0为指定第一个subportfolio,1为指定第二个subportfolio，默认为0。
    返回
        Order对象或者None, 如果创建委托成功, 则返回Order对象, 失败则返回None
'''
##
order_value(security, value, style=None, side='long', pindex=0)

'''
    order_target_value ­ 目标价值下单
    调整股票仓位到value价值，金融期货暂不支持该API
    参数
        security: 股票名字
        value: 期望的股票最终价值
        style: 参见order styles, None代表MarketOrder
        side: ‘long’/’short’，平空单还是多单。默认为多单，股票、基金暂不支持开空单。
        pindex: 在使用set_subportfolios创建了多个仓位时，指定subportfolio的序号, 从0开始,比如0为指定第一个subportfolio,1为指定第二个subportfolio，默认为0
    返回
        Order对象或者None, 如果创建委托成功, 则返回Order对象, 失败则返回None
'''
##
order_target_value(security, value, style=None, side='long', pindex=0)

'''
    cancel_order ­ 撤单
    取消订单
    参数
        order: Order对象或者order_id
    返回
        Order对象或者None, 如果取消委托成功, 则返回Order对象, 委托不存在返回None
'''
##
cancel_order(order)

'''
    get_open_orders ­ 获取未完成订单
    获得当天的所有未完成的订单
    参数
        无
    返回
       返回一个dict, key是order_id, value是Order对象
'''
##
get_open_orders()

'''
    get_orders ­ 获取订单信息
    获取当天的所有订单
    参数
        无
    返回
       返回一个dict, key是order_id, value是Order对象
'''
##
get_orders()

'''
    get_trades ­ 获取成交信息
    获取当天的所有成交记录, 一个订单可能分多次成交
    参数
        无
    返回
       返回一个dict, key是order_id, value是Order对象
'''
##
get_trades()

















