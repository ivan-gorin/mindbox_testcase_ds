import numpy as np

MAX_GROUP_ID = 63

def get_customers_per_group(n_customers, n_first_id=0):
    '''
    Returns an ndarray of shape (64,) with the number of customers per group.
    '''
    if n_first_id != 0:
        return (get_customers_per_group(n_customers + n_first_id)
        - get_customers_per_group(n_first_id))

    answers_for_nines = {}

    def recursive(customer_id):
        nonlocal answers_for_nines
        result = np.zeros(MAX_GROUP_ID+1, dtype=int)
        # Если длина customer_id равна 1, то возвращаем в ручную заполненный массив
        if len(customer_id) == 1:
            for i in range(int(customer_id) + 1):
                result[i] += 1
            return result
        # Считаем ответ для числа из девяток длиной на 1 меньше чем customer_id.
        # Сохраняем ответы в словарь, так как иначе будем много раз пересчитывать одно и то же
        lower_num = '9' * (len(customer_id) - 1)
        if lower_num not in answers_for_nines:
            answers_for_nines[lower_num] = recursive(lower_num)
        lower_ans = answers_for_nines[lower_num]
        # сдвигаем этот ответ на 0, 1, ... , a-1 вправо и прибавляем к ответу
        for i in range(int(customer_id[0])):
            result += np.roll(lower_ans, i)
        # считаем ответ для числа customer_id[1:], сдвигаем его на a вправо и прибавляем к ответу
        if customer_id[1:] in answers_for_nines:
            result += np.roll(answers_for_nines[customer_id[1:]], int(customer_id[0]))
        else:
            result += np.roll(recursive(customer_id[1:]), int(customer_id[0]))
        return result

    customers_per_group = recursive(str(n_customers - 1))
    return customers_per_group
