# Sneaker data variables

purchase_date = input("Purchase date?: ")
retailer = input("Retailer?: ")
release_date = input("Release date?: ")
size = input("What size?: ")
brand = input("Brand?: ")
model = input("Model?: ")
color_way = input("CW?: ")
sku = input("Sku?: ")
retail = input("What did you pay?: ")
resale = input("Whats it worth?: ")
quantity = int(input("Quantity?: "))
profit_per = int(resale) - int(retail)
profit = (int(resale) - int(retail)) * quantity
