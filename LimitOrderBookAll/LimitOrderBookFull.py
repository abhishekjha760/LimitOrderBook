import logging
logging.basicConfig(level = logging.DEBUG)

def buyordr(size):
    
  
    global askordr
    
    if len(askordr) == 0:
        bdordr.append([odrid, float('inf'), size])
        bdordr.sort(key = bid_sort, reverse=True)

    
    index = 0
    while size > 0 and index < len(askordr):
        askordr_price = askordr[index][1]
        askordr_size = askordr[index][2]
        temp = size
        size = size - askordr_size
        askordr[index][2] -= temp
        index += 1

    
    if size > 0:
        bdordr.append([odrid, float('inf'), size])
        bdordr.sort(key = bid_sort, reverse = True)

    
    index = 0
    while index < len(askordr):
        price = askordr[index][2]
        if price <= 0:
            askordr.pop(index)
        else:
            index += 1



def sell_order(size):
   
    global odrid

    if len(bdordr) == 0:
        askordr.append([odrid, float('-inf'), size])
        askordr.sort(key=bid_sort)

    
    index = 0
    while size > 0 and index < len(bdordr):
        bdordr_price = bdordr[index][1]
        bdordr_size = bdordr[index][2]
        temp = size
        size = size - bdordr_size
        bdordr[index][2] -= temp
        index += 1

    # If the bdordr(bid order) doesn't get fulfilled
    if size > 0:
        askordr.append([odrid, float('-inf'), size])
        askordr.sort(key=bid_sort, reverse=True)

    # Check the price if any value from ask has become 0
    index = 0
    while index < len(bdordr):
        price = bdordr[index][2]
        if price <= 0:
            bdordr.pop(index)
        else:
            index += 1

def place_order():
   
    print("In Place Order")
    action = int(input("\n What order you want to place? \n 1. Buy \n 2. Sell \n"))

    if action == 1:
        size = int(input("Enter the size of Share : "))
        buyordr(size)
    elif action == 2:
        size = int(input("Enter the size of Share : "))
        sell_order(size)
    else:
        logging.warning("Number is incorrect. Please enter the number between 1 and 2")

def sort_values(e):
    
    return e[1]

def buy_limit_order(price, size):
   
    # Check whether if there exist any seller in order book
    global odrid

    if len(askordr) == 0:
        bdordr.append([odrid, price, size])
        bdordr.sort(key=sort_values, reverse=True)
        return

    
    index = 0
    while size > 0 and index < len(askordr):
        askordr_price = askordr[index][1]
        askordr_size = askordr[index][2]

        if price >= askordr_price:
            temp = size
            size = size - askordr_size
            askordr[index][2] -= temp
        index += 1

    # If the bdordr(bid order) isn't get fulfilled
    if size > 0:
        bdordr.append([odrid, price, size])
        bdordr.sort(key = sort_values, reverse = True)

    # Check to price if any value from ask has become 0
    index = 0
    while index < len(askordr):
        price = askordr[index][2]
        if price <= 0:
            askordr.pop(index)
        else:
            index += 1

def sell_limit_order(price, size):
    
    # Check whether if there exist any seller in order book
    global odrid
    bdordr=1
    if len(bdordr) == 0:
        askordr.append([odrid, price, size])
        askordr.sort(key = sort_values)
        return

    # Iterate over askordr to fulfill the bdordr
    index = 0
    while size > 0 and index < len(bdordr):
        bdordr_price = bdordr[index][1]
        bdordr_size = bdordr[index][2]

        if price <= bdordr_price:
            temp = size
            size = size - bdordr_size
            bdordr[index][2] -= temp
        index += 1

    # If the sell_order isn't get fulfilled
    if size > 0:
        askordr.append([odrid, price, size])
        askordr.sort(key = sort_values)

    # Check to price if any value from bid  has become 0
    index = 0
    while index < len(bdordr):
        price = bdordr[index][2]
        if price <= 0:
            bdordr.pop(index)
        else:
            index += 1


def limit_order():
    
    action = int(input("\n What order you want to place? \n 1. Buy \n 2. Sell \n"))
    if action == 1:
        price, size = list(map(float,input("Enter the price at which you want to Buy and Size : ").split(" ")))
        buy_limit_order(price, int(size))
    elif action == 2:
        price, size = list(map(float,input("Enter the price at which you want to Sell and Size : ").split(" ")))
        sell_limit_order(price, int(size))
    else:
        logging.warning("Number is incorrect. Please enter the number between 1 and 2")

def cancel_order(arr, odrid):
   
    for index, val in enumerate(arr):
        if val[0] == odrid:
            arr.pop(index)
            return
    logging.error("This odrid doesn't exist \n")


def helper_cancel_order():
    
    print("Enter the order id of your Order : ")
    order_no = int(input())
    print("Enter the Order Type i.e Buy or Sell ? ")
    order_type = input().lower()
    if order_type == 'buy':
        cancel_order(bdordr, order_no)
    elif order_type == 'sell':
        cancel_order(askordr, order_no)
    else:
        logging.warning("Please enter the type between Buy or Sell ")


def numbers_to_string(argument):
   
    switcher = {
        1 : place_order,
        2 : limit_order,
        3 : helper_cancel_order
    }

    return switcher.get(argument, 'Number is incorrect. Enter between 1 and 3')()


odrid = 0
askordr = []
bdordr = []

while True:
    print("\nWhat to perform\n 1. Place Market Order\n 2. Place Limit Order\n 3. Stop Particular Order\n")
    action = int(input("Enter the number of what you want to perform: "))
    odrid += 1
    numbers_to_string(action)
    print("Ask Order = ",askordr)
    print("Bid Order", bdordr)