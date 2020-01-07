import datetime


def logger_with_path(path):
    def logger(old_func):
        def func_decorated(*args, **kwargs):

            call_time = datetime.datetime.now()
            output = old_func(*args, **kwargs)

            with open(path, 'a', encoding='utf-8') as log:
                log.write('\n\n')
                log.write(str(call_time) + '\n')
                log.write('func_name: ' + old_func.__name__ + '\n')
                log.write('args: ' + str(args) + '\n')
                log.write('kwargs: ' + str(kwargs) + '\n')
                log.write('result: ' + str(output))

        return func_decorated
    return logger
