# import random
# from faker import Faker 

# fake = Faker()

# def generate_po_number():
#     letters = string.ascii_uppercase
#     # Generate two random capital letters
#     random_letters = ''.join(random.choices(letters, k=2))
    
#     # Generate unique four-digit number
#     digits = [str(x) for x in range(10)]
#     random.shuffle(digits)
#     unique_digits = ''.join(digits[:4])

#     # Concatenate letters and digits to form the PO number
#     po_number = f"{random_letters}{unique_digits}"
#     return po_number


# def generate_dummy_vendor_data(num):
#     for i in range(num):
#         name = fake.company()
#         contact_details = fake.phone_number()
#         address = fake.address()
#         vendor_code = fake.uuid4()  # Generates a random UUID as a vendor code
#         on_time_delivery_rate = round(random.uniform(80, 100), 2)  # Random float between 80 and 100
#         quality_rating_avg = round(random.uniform(2, 5), 2)  # Random float between 2 and 5 for quality rating
#         average_response_time = round(random.uniform(1, 24), 2)  # Random float between 1 and 24 hours
#         fulfillment_rate = round(random.uniform(70, 100), 2)  # Random float between 70 and 100

#         Vendor.objects.create(
#             name= name,
#             contact_details= contact_details,
#             address= address,
#             vendor_code= vendor_code,
#             on_time_delivery_rate= on_time_delivery_rate,
#             quality_rating_avg= quality_rating_avg,
#             average_response_time= average_response_time,
#             fulfillment_rate= fulfillment_rate,
#         )

# def generate_dummy_purchase_orders(num_records):
#     vendors = Vendor.objects.all()  # Fetching existing vendors or use your logic to retrieve them

#     for _ in range(num_records):
#         vendor = random.choice(vendors)  # Randomly select a vendor
#         po_number = generate_po_number()  # Generate a random PO number using Faker

#         order_date = fake.date_time_this_month(before_now=True, after_now=False)
#         delivery_date = order_date + timedelta(days=random.randint(1, 30))

#         # Generate dummy items in JSON format
#         items = [
#             {
#                 "item_name": fake.word(),
#                 "price": round(random.uniform(10, 100), 2),
#                 "quantity": random.randint(1, 20),
#             }
#             for _ in range(random.randint(1, 5))
#         ]

#         quantity = sum(item["quantity"] for item in items)

#         status_options = ["Pending", "Completed", "Canceled"]
#         status = random.choice(status_options)

#         issue_date = fake.date_time_this_month(before_now=True, after_now=False)
#         acknowledgment_date = delivery_date + timedelta(days=random.randint(-5, 5)) if status == "Completed" else None

#         # Creating a PurchaseOrder object with dummy data
#         PurchaseOrder.objects.create(
#             po_number=po_number,
#             vendor=vendor,
#             order_date=order_date,
#             delivery_date=delivery_date,
#             items=items,
#             quantity=quantity,
#             status=status,
#             issue_date=issue_date,
#             acknowledgment_date=acknowledgment_date
#         )

# # Generating 10 dummy purchase orders
# # generate_dummy_purchase_orders(4)

# def generate_dummy_performance_records(num_records):
#     vendors = Vendor.objects.all()  # Fetching existing vendors or use your logic to retrieve them

#     for _ in range(num_records):
#         vendor = random.choice(vendors)  # Randomly select a vendor
#         date = fake.date_time_this_year(before_now=True, after_now=False)  # Generate a random date within the current year

#         on_time_delivery_rate = round(random.uniform(80, 100), 2)  # Random on-time delivery rate
#         quality_rating_avg = round(random.uniform(3, 5), 2)  # Random quality rating average
#         average_response_time = round(random.uniform(1, 10), 2)  # Random average response time
#         fulfillment_rate = round(random.uniform(90, 100), 2)  # Random fulfillment rate

#         # Creating a PerformanceRecord object with dummy data
#         HistoricalPerformance.objects.create(
#             vendor=vendor,
#             date=date,
#             on_time_delivery_rate=on_time_delivery_rate,
#             quality_rating_avg=quality_rating_avg,
#             average_response_time=average_response_time,
#             fulfillment_rate=fulfillment_rate
#         )


# # Generating 10 dummy performance records
# # generate_dummy_performance_records(10)




# def calculate_on_time_delivery_rate():
#     # Retrieve all purchase orders
#     all_purchase_orders = PurchaseOrder.objects.all()

#     total_orders = 0
#     on_time_orders = 0

#     for order in all_purchase_orders:
#         total_orders += 1

#         # Assuming delivery_date is the expected delivery date of the order
#         # and order_date is the date when the order was placed
#         if order.delivery_date <= order.order_date + timedelta(days=1):
#             # If the delivery_date is on or before the promised date (considering a 1-day buffer)
#             on_time_orders += 1

#     if total_orders > 0:
#         on_time_delivery_rate = (on_time_orders / total_orders) * 100
#         return on_time_delivery_rate
#     else:
#         return 0  # If there are no orders, return 0 as the delivery rate
    

# def calculate_quality_rating(vendor_name):
#     try:
#         # Retrieve the vendor using the provided name
#         vendor = Vendor.objects.get(name=vendor_name)

#         # Retrieve all purchase orders for the specified vendor with quality ratings
#         orders_with_ratings = vendor.purchase_orders.filter(quality_rating__isnull=False)
        
#         total_ratings = orders_with_ratings.aggregate(total=Sum('quality_rating'))['total']
#         total_orders_with_ratings = orders_with_ratings.count()
        
#         if total_orders_with_ratings > 0 and total_ratings is not None:
#             average_quality_rating = total_ratings / total_orders_with_ratings
#             return average_quality_rating
#         else:
#             return 0  # If no quality ratings are available, return 0 as the average rating

#     except Vendor.DoesNotExist:
#         return 0  # If the 
