from random import randint as r
import sqlite3

"""Creating Credit Card Account"""

bank_id = '400000'
customer_id = ''
check_sum = ''
balance = 0
card_num = ''
card_pin = ''

conn = sqlite3.connect('card.s3db')  # connection to SQL DB
cur = conn.cursor()  # cursor method allows for SQL queries
# cur.execute('SELECT * ...') ---> execute SQL query
# conn.commit() ---> saves queries to DB
# cur.fetchone() ---> returns first row from response/query
# cur.fetchall() ---> returns all rows from response/query
try:
    cur.execute('''CREATE TABLE card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)''')
    conn.commit()
except:
    pass


def card_and_pin():
    global card_num, customer_id, check_sum, card_pin
    card_pin = r(1000, 9999)

    while True:
        customer_id = str(r(100000000, 999999999))
        potential_card = bank_id + customer_id
        luhn_check = [int(x) for x in potential_card]

        for i in range(0, 15, 2):
            luhn_check[i] *= 2

        luhn_check = [x - 9 if x > 9 else x for x in luhn_check]
        check_sum = str(10 - int(str(sum(luhn_check))[1]))

        if check_sum == '10':
            continue

        else:
            card_num = int(potential_card + check_sum)
            cur.execute(f'''INSERT INTO card (number, pin) VALUES ({str(card_num)}, {str(card_pin)})''')
            conn.commit()
            break


def create_account():
    global card_num, card_pin
    card_and_pin()
    print(f'\nYour card has been created\nYour card number:\n{card_num}\nYour card PIN:\n{card_pin}\n')


def check_luhn(y):
    luhn = [int(i) for i in y]
    ch_sum = luhn.pop(-1)

    for i in range(0, 15, 2):
        luhn[i] *= 2

    luhn = [z - 9 if z > 9 else z for z in luhn]
    luhn = sum(luhn)
    if (luhn + ch_sum) % 10 != 0:
        return False
    return True


def transfer_funds(num):
    while True:
        print('\nTransfer')
        rec = input('Enter card number:\n')
        
        # checking luhn algorithm
        if check_luhn(rec) is False:
            print('Probably you made a mistake in the card number. Please try again!\n')
            break

        # checking card numbers aren't the same
        if rec == num:
            print('You can\'t transfer money to the same account!\n')
            break

        # checking if card number is in db
        cur.execute(f'SELECT number FROM card WHERE number = "{rec}"')
        result = cur.fetchone()
        if result is None:
            print('Such a card does not exist!\n')
            break

        funds = int(input('Enter how much money you want to transfer\n'))

        # checking if user has enough funds
        cur.execute(f'SELECT balance FROM card WHERE number = {num}')
        bal = cur.fetchone()[0]
        if bal < funds:
            print('Not enough money!\n')
            break

        # executing transfer if all else looks good
        cur.execute(f'UPDATE card SET balance = balance + {funds} WHERE number = "{rec}"')
        conn.commit()
        cur.execute(f'UPDATE card SET balance = balance - {funds} WHERE number = {num}')
        conn.commit()
        break


def login_menu(x):
    while True:
        cur.execute(f'SELECT balance FROM card WHERE number = {x}')
        bal = cur.fetchone()[0]

        menu_choice = int(input('\n1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n'))

        #checking the balance of an account
        if menu_choice == 1:  
            print(f'\nBalance: {bal}')
            continue

        # deposit funds into your account
        elif menu_choice == 2:
            deposit = int(input('\nEnter income:\n'))
            cur.execute(f'UPDATE card SET balance = (balance + {deposit}) WHERE number = {x}')
            conn.commit()
            print('Income was added!')

        # transferring funds to another account
        elif menu_choice == 3:
            transfer_funds(x)

        # close account
        elif menu_choice == 4:  
            cur.execute(f'DELETE FROM card WHERE number = {x}')
            conn.commit()
            print('\nThe account has been closed!\n')
            break

        # logout
        elif menu_choice == 5:  
            print('\n')
            break

        # quit the program
        else:
            quit()

    return False


def login():
    cur.execute('SELECT number, pin FROM card')
    result = cur.fetchall()
    while True:
        login_card = input('\nEnter your card number:\n')
        login_pin = input('Enter your PIN:\n')
        for i in range(len(result)):
            if login_card in result[i] and login_pin in result[i]:
                print('\nYou have successfully logged in!')
                while True:
                    login_menu(login_card)
                    return False
        print('\nWrong card number or PIN!\n')
        break


def jp_bank():
    while True:
        main_menu = int(input('1. Create an account\n2. Log into account\n0. Exit\n'))

        if main_menu == 1:
            create_account()
            continue

        elif main_menu == 2:
            login()

        elif main_menu == 0:
            print('\nThanks for banking with us!\nBye Bye For Now!')
            conn.commit()
            conn.close()
            quit()


if __name__ == '__main__':
    jp_bank()
