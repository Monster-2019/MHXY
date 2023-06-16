from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import EmptyInputValidator

def select_daily():
    daily_type = inquirer.select(
        message="请选择日常类型：",
        choices=[
            Choice(1, name="1. 五开副本日常"),
            Choice(2, name="2. 五开日常"),
            Choice(3, name="3. 单人副本日常"),
            Choice(4, name="4. 单人日常")
        ],
        transformer= lambda result: result[3:],
    ).execute()
    return daily_type

def select_single():
    single_task = inquirer.select(
        message="请选择单任务：",
        choices=[
            Choice(1, name="1. 帮派"),
            Choice(2, name="2. 工坊"),
            Choice(3, name="3. 经验链"),
            Choice(4, name="4. 队长无限鬼")
        ],
        transformer= lambda result: result[3:],
    ).execute()
    return single_task

def initInquirer():
    answers = []
    func = inquirer.select(
        message="请选择功能：",
        choices=[
            Choice(1, name="1. 一键"),
            Choice(2, name="2. 日常"), 
            Choice(3, name="3. 单任务"),
            Choice(0, name="4. 退出")
        ],
        transformer= lambda result: result[3:],
    ).execute()

    answers.append(func)

    if func == 0:
        return 0
    elif func == 1:
        pass
    elif func == 2:
        daily_type = select_daily()
        answers.append(daily_type)
    elif func == 3:
        single_task = select_single()
        answers.append(single_task)

        if single_task == 4:
            ghost_count = inquirer.number(
                message="请输入无限鬼次数",
                min_allowed=1,
                max_allowed=25,
                default=25,
                validate=EmptyInputValidator(),
                instruction="(默认25轮)",
            ).execute()
            answers.append(ghost_count)


initInquirer()