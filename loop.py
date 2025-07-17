import concurrent.futures

# Define the tasks for each list (each will run independently)
def process_list1():
    for item in [1, 2, 3, 4]:
        print(f'List 1 item: {item}')

def process_list2():
    for item in ['a', 'b', 'c', 'd']:
        print(f'List 2 item: {item}')

def process_list3():
    for item in [True, False, True, False]:
        print(f'List 3 item: {item}')

def process_list4():
    for item in [0.1, 0.2, 0.3, 0.4]:
        print(f'List 4 item: {item}')

# Run the loops concurrently
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.submit(process_list1)
    executor.submit(process_list2)
    executor.submit(process_list3)
    executor.submit(process_list4)
