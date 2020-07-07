# 创建一个用于接收结果的进程
def result_handler(result_queue):
    while True:
        search_result = result_queue.get()

        # 查重结果处理
        print(search_result)
        print("处理完毕")