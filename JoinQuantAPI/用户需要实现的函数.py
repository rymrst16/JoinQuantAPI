#用户需要实现的函数

'''官方解释'''
#结合其他地方补充

"""
    关于所有函数的解释：
    1.所有市价单下单之后同步完成(也即order_XXX系列函数返回时完成),context.portfolio会同步变化
    2.如果实际价格已经涨停或者跌停, 则相对应的买单或卖单不成交,市价单直接取消(log中有警告信息), 限价单会挂单直到可以成交
    3.一天结束后, 所有未完成的订单会被取消
    4.每次订单完成(完全成交)或者取消后, 我们会根据成交量计算手续费(参见set_order_cost),减少您的现金
    5.同一个时间点总是先运行run_XXX指定的函数,然后是before_trading_start,handle_data和after_trading_end
    6.模拟盘在每天运行结束后会保存状态, 结束进程(相当于休眠). 然后在第二天恢复.
    进程结束时会保存这些状态:
        用户账户, 持仓
        使用 pickle 保存 g 对象.注意
            g 中以 ‘__’ 开头的变量将被忽略, 不会被保存
            g 中不能序列化的变量不会被保存, 重启后会不存在.正确的做法是, 在 process_initialize 中初始化它, 并且名字以 ‘__’ 开头
            涉及到IO(打开的文件, 网络连接, 数据库连接)的对象是不能被序列化的
            使用 pickle 保存 context 对象, 处理方式跟 g 一样
            为了兼容老旧的代码,我们会保存在函数外定义的全局变量.但是不推荐大家直接使用全局变量
    恢复过程是这样的:
        1. 加载策略代码,因为python是动态语言, 编译即运行, 所以全局的(在函数外写的)代码会被执行一遍.
        2. 使用保存的状态恢复 g, context, 和函数外定义的全局变量.
        3. 执行 process_initialize, 每次启动时都会执行这个函数.
        4. 如果策略代码和上一次运行时发生了修改，而且代码中定义了after_code_changed 函数，则会运行 after_code_changed 函数。
    7.强烈建议模拟盘使用真实价格成交,即调用set_option('use_real_price',True).更多细节请看 set_option
"""

'''
    初始化方法，在整个回测、模拟实盘中最开始执行一次，用于初始一些全局变量
    参数
        context: Context对象, 存放有当前的账户/股票持仓信息
    返回
        None
'''
##
def initialize(context):
    # g为全局变量
    g.security = "000001.XSHE"

    '''
    设置基准
    默认我们选定了沪深300指数的每日价格作为判断您策略好坏和一系列风险值计算的基准.您也可以使用set_benchmark指定其他股票/指数/ETF的价格作为基准。注意：这个函数只能在initialize中调用
    参数
        security:股票/指数/ETF代码
    返回
        None
    '''
    set_benchmark('000300.XSHG')

    '''
    set_order_cost(cost, type)设置佣金/印花税
    指定每笔交易要收取的手续费, 系统会根据用户指定的费率计算每笔交易的手续费
    参数
        cost: OrderCost 对象
            open_tax，买入时印花税 (只股票类标的收取，基金与期货不收)
            close_tax，卖出时印花税 (只股票类标的收取，基金与期货不收)
            open_commission，买入时佣金
            close_commission, 卖出时佣金
            close_today_commission, 平今仓佣金
            min_commission, 最低佣金，不包含印花税
        type: 股票、基金或金融期货，’stock’/ ‘fund’ / ‘index_futures’
    返回
        None
    '''
    # 默认：股票类每笔交易时的手续费是：买入时佣金万分之三，卖出时万佣金分之三加千分之一印花税, 每笔交易佣金最低扣5块钱
    set_order_cost(OrderCost(open_tax=0, close_tax=0.001, open_commission=0.0003,close_commission=0.0003, close_today_commission=0, min_commission=5), type='stock')

    '''
    set_slippage(object)设置滑点
    回测/模拟时有效.
    当您下单后, 真实的成交价格与下单时预期的价格总会有一定偏差,因此我们加入了滑点模式来帮您更好的模拟真实市场的表现. 我们暂时只支持固定滑点
    注：如果您没有调用 set_slippage 函数, 系统默认的滑点是 PriceRelatedSlippage(0.00246)
    固定滑点：
    当您使用固定滑点的时候,我们认为您的落单的多少并不会影响您最后的成交价格.您只需要指定一个价差,当您下达一个买单指令的时候, 成交的价格等于当时(您执行order函数所在的单位时间)的平均价格加上价差的一半；当您下达一个卖出指令的时候，卖出的价格等于当时的平均价格减去价差的一半.价差可以设定为一个固定值或者按照百分比设定。
    固定值：
    这个价差可以是一个固定的值(比如0.02元, 交易时加减0.01元), 设定方式为：set_slippage(FixedSlippage(0.02))
    百分比：
    这个价差可以是是当时价格的一个百分比(比如0.2%, 交易时加减当时价格的0.1%), 设定方式为：
    set_slippage(PriceRelatedSlippage(0.002))
    '''
    # 设定滑点为固定值
    set_slippage(FixedSlippage(0.02))

    '''
    set_option ­ 设置其他项
    set_option(name, value)
    设置 真实价格、成交量比例、期货保证金比例选项,其中name=’use_real_price’时必须在initialize中调用，其它name没有这样的限制。
    参数
        name: 选项名字, 字符串
        value: 选项的值, 根据name的不同, 是不同的类型
    返回
        None
    
    共有如下选项：
        1.use_real_price(真实价格回测): value是True/False.是否使用真实价格回测.原理讲解图示见帖子(https://www.joinquant.com/post/1629)。默认是False(主要是为了让旧的策略不会出错).
        为了更好的模拟, 建议大家都设成 True. 将来对接实盘交易时, 此选项会强制设成 True
        2.order_volume_ratio(设定成交量比例):value是一个float值,根据实际行情限制每个订单的成交量.
    '''
    set_benchmark('use_real_price',True)

'''
    该函数每个单位时间会调用一次,如果按天回测,则每天调用一次,如果按分钟,则每分钟调用一次
    该函数在回测中的非交易日是不会触发的（如回测结束日期为1月5日，则程序在1月1日­3日时，handle_data不会运行，4日继续运行）。
    参数
        context: Context对象, 存放有当前的账户/标的持仓信息
        data: 一个字典(dict), key是股票代码, value是当时的SecurityUnitData 对象. 存放前一个单位时间(按天回测, 是前一天, 按分钟回测, 则是前一分钟) 的数据. 注意:
        1.为了加速, data 里面的数据是按需获取的, 每次 handle_data 被调用时, 
        2.data 是空的 dict, 当你使用data[security] 时该 security 的数据才会被获取.data只在这一个时间点有效,请不要存起来到下一个handle_data 再用
        3.注意, 要获取回测当天的开盘价/是否停牌/涨跌停价, 请使用 get_current_data
    返回
        None
'''
##context.portfolio中的持仓价格会使用当天开盘价更新
##data是昨天的按天数据, 要想拿到当天开盘价,请使用get_current_data拿取day_open字段
def handle_data(context, data):
    order("000001.XSHE",100)

'''
    该函数会在每天开始交易前被调用一次, 您可以在这里添加一些每天都要初始化的东西
    参数
        context: Context对象, 存放有当前的账户/股票持仓信息
    返回
        None
'''
##
def before_trading_start(context):
    log.info(str(context.current_dt))

'''
    该函数会在每天结束交易后被调用一次,您可以在这里添加一些每天收盘后要执行的内容.这个时候所有未完成的订单已经取消.
    参数
        context: Context对象, 存放有当前的账户/股票持仓信息
    返回
        None
'''
##
def after_trading_end(context):
    log.info(str(context.current_dt))

'''
    该函数会在每次模拟盘/回测进程重启时执行,一般用来初始化一些不能持久化保存的内容.在initialize后执行.因为模拟盘会每天重启, 所以这个函数会每天都执行.
    参数
        context: Context对象, 存放有当前的账户/股票持仓信息
    返回
        None
'''
##
def process_initialize(context):
    # query 对象不能被 pickle 序列化, 所以不能持久保存, 所以每次进程重启时都给它初始化
    # 以两个下划线开始, 系统序列化 [g] 时就会自动忽略这个变量, 更多信息, 请看 [g] 和 [模拟盘注意事项]
    g.__q = query(valuation)

'''
    模拟盘在每天的交易时间结束后会休眠，第二天开盘时会恢复，如果在恢复时发现代码已经发生了修改，则会在恢复时执行这个函数。具体的使用场景：可以利用这个函数修改一些模拟盘的数据。注意:因为一些原因,执行回测时这个函数也会被执行一次,在process_initialize 执行完之后执行
    参数
        context: Context对象, 存放有当前的账户/股票持仓信息
    返回
        None
'''
##
def after_code_changed(context):
    g.stock = '000001.XSHE'
