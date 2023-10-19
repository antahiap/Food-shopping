import json
import gkeepapi
import keyring
import os

from dotenv import load_dotenv
load_dotenv()


def merge_food(ids):
    shopList = {"ingredients": [], "meals": []}

    with open('recepies.json') as f:
        data = json.load(f)
        foods = data["foods"]

    pick_order = [8, 7, 2, 1, 4, 3, 6, 5]
    # pick_order = [8, 7, 2, 1, 4, 3, 6, 5]

    for f in foods:
        id = f["id"]
        if id in ids:
            items = f["ingredients"]
            shopList["meals"].append(f["name"])
            for i in items:
                name = i["item"]
                a = list(item for item in shopList["ingredients"] if item["item"] == name)
        #         if name in shopList["ingredients"]:
        #             shopList[i] += i[amount]
                if len(a) == 0:
                    shopList["ingredients"].append(i)
                    i['grp'] = pick_order.index(i['grp'])
                else:
                    A = next(item for item in shopList["ingredients"] if item["item"] == name)
                    A['amount'] += i["amount"]
        # else:
        #     print(id)
    out_string = ', '.join(shopList['meals'])
    out_list = [', '.join(shopList['meals'])]
    sorted_list = sorted(shopList["ingredients"], key=lambda k: k['grp'])
    for item in sorted_list:

        # print(item)
        out_string += ('{0:<20}{1:<4}{2}\n'.format(item["item"], item["amount"], item["unit"]))
        out_list.append('{0:<20}{1:<4}{2}'.format(item["item"], item["amount"], item["unit"]))
    return(out_list)


def to_gkeep(inList, email='p.anahita@gmail.com'):

    keep = gkeepapi.Keep()
    token = keyring.get_password('google-keep-token', 'p.anahita')
    keep.resume(email, token)

    # glist = keep.createList('Test', [('1', False), ('2', True)])

    glist = keep.get(os.getenv('GOOGLE_KEEP'))
    [gl.delete() for gl in glist.items]

    for il in inList:
        glist.add(il, False, gkeepapi.node.NewListItemPlacementValue.Bottom)

    keep.sync()
    print(glist)


def login_gkeep():
    import getpass

    try:
        keep = gkeepapi.Keep()
        user = input("Username: ")
        p = getpass.getpass()
        keep.login(user, p)
        token = keep.getMasterToken()
        keyring.set_password('google-keep-token', 'p.anahita', token)
        print('wait for syncing')
        keep.sync()
    except gkeepapi.exception.LoginException:
        print('Wrong username or pass.')


if __name__ == '__main__':

    ids = ["0001", "0002", "0003"]
    ids = ["0003", "0004", "0005"]
    ids = ["0006", "0007", "0008"]

    ids = ["0001", "0003", "0008"]
    ids = ["0009", "0010", "0005"]
    ids = ["0004", "0007", "0009"]
    ids = ["0010", "0007", "0008"]
    ids = ["0001"]

    mergeList = merge_food(ids)
    # print(mergeList)
    # login_gkeep()

    to_gkeep(mergeList)

# from urllib.request import urlopen
# import ssl
# from bs4 import BeautifulSoup

# url = "http://kite.com"
# url = "https://www.hellofresh.com/recipes/de-mozzarella-crusted-chicken-w0-5845b27b2e69d7646110f1c2"
# # Ignore SSL certificate errors
# ctx = ssl.create_default_context()
# ctx.check_hostname = False
# ctx.verify_mode = ssl.CERT_NONE
# document = urlopen(url, context=ctx)

# html = document.read()
# if document.getcode() != 200 :
#     print("Error on page: ",document.getcode())
#     cur.execute('UPDATE Pages SET error=? WHERE url=?', (document.getcode(), url) )
#
# if 'text/html' != document.info().get_content_type() :
#     print("Ignore non text/html page")
#     cur.execute('DELETE FROM Pages WHERE url=?', ( url, ) )
#     cur.execute('UPDATE Pages SET error=0 WHERE url=?', (url, ) )
#     conn.commit()
#
#     print('('+str(len(html))+')', end=' ')
# soup = BeautifulSoup(html)
#
# for script in soup(["script", "style"]):
#     script.decompose()
#
#
# strips = list(soup.stripped_strings)
# print(strips)
