import requests

# nick = 'Jollu8'
# # Define the URL
# url = f"https://leetcode-api-faisalshohag.vercel.app/{nick}"
# s = 'https://leetcode.com/graphql?query=query { userContestRanking(username:' + '"' +nick+'"' + ') { attendedContestsCount rating globalRanking totalParticipants topPercentage } }'
# # Send a GET request to the URL
# response = requests.get(url)
# response1 = requests.get(s)
#
# # Get the JSON data from the response
# data = response.json()
# data1 = response1.json()
#
# print(data)
# print(data1)
# print(data1['data']['userContestRanking']['rating'])

# from models.base import conn
#
# cur = conn.cursor()
# cur.execute(f"SELECT * FROM users WHERE user_id={1144427229}")
# rows = cur.fetchall()
# print(rows)


def create_unicode_table(data):
    # Символы для создания рамки
    h_line = '─'
    v_line = '│'
    tl_corner = '┌'
    tr_corner = '┐'
    bl_corner = '└'
    br_corner = '┘'
    t_join = '┬'
    b_join = '┴'
    l_join = '├'
    r_join = '┤'
    cross = '┼'

    # Определение ширины колонок
    col_widths = [max(len(str(row[i])) for row in data) for i in range(len(data[0]))]

    # Создание заголовка
    header = f"{tl_corner}{t_join.join(h_line * (w + 2) for w in col_widths)}{tr_corner}\n"
    header += f"{v_line} " + f" {v_line} ".join(f"{data[0][i]:<{col_widths[i]}}" for i in range(len(data[0]))) + f" {v_line}\n"
    header += f"{l_join}{cross.join(h_line * (w + 2) for w in col_widths)}{r_join}\n"

    # Создание строк данных
    rows = []
    for row in data[1:]:
        rows.append(f"{v_line} " + f" {v_line} ".join(f"{str(row[i]):<{col_widths[i]}}" for i in range(len(row))) + f" {v_line}\n")

    # Создание нижней границы
    footer = f"{bl_corner}{b_join.join(h_line * (w + 2) for w in col_widths)}{br_corner}\n"

    # Объединение всех частей
    return header + ''.join(rows) + footer

# Пример использования
data = [
    ['№', 'Имя', 'Имя'],
    [1, 'SatoruGodjo', 1753.076],
    [2, 'ulansyn', 1620.786],
    [3, 'Jollu8', 0]
]

print(create_unicode_table(data))