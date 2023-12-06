# # # 300201129 Sübhan Akbenli 
# # i am using python 3.11.6 version :)

def printMenu(liste):
    """
    Display a menu based on the provided list.
    Parameters:
    - liste (list): A list containing items to be displayed in the menu.
    """
    for row in liste:
        print(row[0], end='. ')
        print(row[1])
        
def prepareInfo(choosen,fileName):
    """Bu fonksiyon, belirli bir dosyadan bilgileri okur ve işler.
    Args:
        choosen (str): İlgili bilgi türünü belirten bir dize.
        fileName (str): İşlenecek dosyanın adı.
    Returns:
        list: Dosyadan alınan ve işlenen bilgileri içeren bir liste.
    """
    with open(fileName, 'r') as f:
            data = f.read()
    data = data.split('\n')
    data = [i.split(';') for i in data]
    if fileName == 'categories.txt' and choosen !=-1:
        categories = [i for i in data if i[0] == choosen]
        return categories

    elif (fileName == 'products.txt' or fileName=="portions.txt") and choosen !=-1:
        products = [i for i in data if i[0] == "#"+choosen]
        return products

    else:
        return data

def getUserInput(text):
    """
    Get user input based on the provided text prompt.
    Parameters:
    - text (str): The type of input to be obtained ("category", "product", "portion", or "continue").
    Returns:
    - int or bool: If the input type is "category", "product", or "portion", returns an integer.
                   If the input type is "continue", returns a boolean.
    Raises:
    - ValueError: If the user enters a non-integer value when expecting an integer input.
    """
    if text == "category" or text == "product" or text == "portion":
        while True:
            try:
                userInput = int(input("Please select the {}: ".format(text)))             
                if userInput > 0:
                    return userInput
                else:
                    print("Please enter a valid number")
            except ValueError:
                print("Please enter a valid number")           
    else:
        output_format = """--------------------------------------------------\n{}"""
        userInput = input(output_format.format("Would you like to complete your order? (y/n) "))
        print("--------------------------------------------------")

        if userInput == "y":
            return True
        elif userInput == "n":
            return False
        else:
            print("Please enter a valid input")


def main():
    try:
        output_format = """--------------------------------------------------
{}
--------------------------------------------------"""
        # Initialize an empty list to store orders
        orders = []
        print(output_format.format('Welcome to the Store'))
        wouldLikeToComplete = False
        
        # Main loop to take user orders
        while not wouldLikeToComplete:
            order = []
            
            # Prepare and display categories
            categories = prepareInfo(-1, 'categories.txt')
            printMenu(categories)
            
            # Get user input for category and retrieve chosen item
            input_category_index = getUserInput("category")
            chosen_item = categories[input_category_index - 1]
            print(output_format.format(chosen_item[1]))
            order.append(chosen_item[1])
            
            # Prepare and display products based on the chosen category
            products = prepareInfo(chosen_item[0], 'products.txt')
            printMenu(enumerate((name for id, name, code in products), start=1))
            
            # Get user input for product and retrieve chosen item
            input_product_index = getUserInput("product")
            chosen_item = products[input_product_index - 1]
            print(output_format.format(chosen_item[1]))
            order.append(chosen_item[1])
            
            # Prepare and display portions based on the chosen product
            portions = prepareInfo(chosen_item[-1], 'portions.txt')
            printMenu(enumerate((name for id, name, price in portions), start=1))
            
            # Get user input for portion and retrieve chosen item
            input_portion_index = getUserInput("portion")
            chosen_item = portions[input_portion_index - 1]
            order.append(chosen_item[1])
            order.append(chosen_item[-1])
            
            # Add the completed order to the list of orders
            orders.append(order)
            
            # Check if the user wants to continue ordering
            wouldLikeToComplete = getUserInput("continue")
        
        # Display the order recipe
        recipe = """Order Recipe
==============================================================
{}
=============================================================="""
        orders_text = "\n".join([" ".join(i) for i in orders])
        print(recipe.format(orders_text))
        
        # Calculate and display the total cost of the orders
        total = sum([float(i[-1]) for i in orders])
        print(f"Total: {total.__round__(2)} TL")
    
    except Exception as e:
        # Handle exceptions and recursively call main() in case of an error
        print(str(e))
        main()
        
main()