arr1 = {'username': '0000',
        'password': '1111',
        'bankcard': '2212',
        'idcard': '3312',
        'bankphone': '44412'}

for k, v in arr1.items():
    print(v)

accounts = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
missions = ['a', 'b', 'c']
task = {}
i = 0
while i < len(accounts):
    for mission in missions:
        if i < len(accounts):
            task[accounts[i]] = mission
            i += 1
        else:
            break
print(task)

kim_dict = {0: "10", 1:"25", 2:"50", 3:"100", 4:"200"}
current = "50"
current_no = None
input_test = "10"
input_test_no = None
for key,value in kim_dict.items():
    if current == value:
        current_no = key
    if input_test == value:
        input_test_no = key
step = input_test_no - current_no
if step is None:
    print("不在这里，凉凉")
elif step > 0:
    print("在当前界面值右边，需要" + str(step) + "步完成")
elif step == 0:
    print("别动，位置刚刚好")
else:
    print("在当前界面值左边，需要" + str(step).split('-')[1] + "步完成")