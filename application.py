#importing the CSV module & easypost module
import csv, easypost, sys

easypost.api_key = 'EZTKb4661e503603421d8dd125dc8e383aa4hY4mwPbdKTnhsCy2CwfUYA'

CALIFORNIA_ADDRESS = {
    'street1': '10731 Walker St',
    'street2': '',
    'city': 'Cypress',
    'state': 'CA',
    'zip_code': 90630,
    'country': 'US'
}

OHIO_ADDRESS = {
    'street1': '4720 Poth Rd',
    'street2': '',
    'city': 'Whitehall',
    'state': 'OH',
    'zip_code': 43213,
    'country': 'US'
}

origin_california = easypost.Address.create(
    street1 = '10731 Walker St',
    street2 = '',
    city = 'Cypress',
    state = 'CA',
    zip = 90630,
    country = 'US'
)

origin_ohio = easypost.Address.create(
    street1 = '4720 Poth Rd',
    street2 = '',
    city = 'Whitehall',
    state = 'OH',
    zip = 43213,
    country = 'US'
)


with open('sample-data.csv', 'r') as csv_file:
    csv_data = csv.reader(csv_file)

    for csv_line in csv_data:
        street1 = csv_line[0]
        street2 = csv_line[1]
        city = csv_line[2]
        state = csv_line[3]
        zip_code = csv_line[4]
        country = csv_line[5]
        height = csv_line[6]
        length = csv_line[7]
        width = csv_line[8]
        weight = csv_line[9]

        to_address = easypost.Address.create(
            street1 = street1,
            street2 = street2,
            city = city,
            state = state,
            zip = zip_code,
            country = country,
        )

        parcel = easypost.Parcel.create(
            length = length,
            width = width,
            height = height,
            weight = weight
        )

        shipment_california = easypost.Shipment.create(
            to_address = to_address,
            from_address = origin_california,
            parcel = parcel
        )

        shipment_ohio = easypost.Shipment.create(
            to_address = to_address,
            from_address = origin_ohio,
            parcel = parcel
        )

        california_rates = []
        ohio_rates = []

        for cali_counter in shipment_california.rates:
            california_rates.append(float(cali_counter.rate))

        for ohio_counter in shipment_ohio.rates:
            ohio_rates.append(float(ohio_counter.rate))

        print("Lowest California: {} @ {}".format(min(california_rates), california_rates.index(min(california_rates))))
        print("Lowest Ohio: {} @ {}".format(min(ohio_rates), ohio_rates.index(min(ohio_rates))))

        print("------------------------")

        print("Highest California: {} @ {}".format(max(california_rates), california_rates.index(max(california_rates))))
        print("Highest Ohio: {} @ {}".format(max(ohio_rates), ohio_rates.index(max(ohio_rates))))

        #print("Cheapest California: " + min(california_rates))
        #print("Cheapest Ohio: " + min(ohio_rates))

        print("------------------------")

        for x in california_rates:
            print(x)

        print("------------------------")

        for y in ohio_rates:
            print(y)

        print("------------------------")

        '''
        print(len(shipment_california.rates))
        print("------------------------")
        print(len(shipment_ohio.rates))
        print('========================')
        print(shipment_california.rates[9])
        print("------------------------")
        print(shipment_ohio.rates[9])
        
        original_stdout = sys.stdout

        out_file = open('output.json', 'w')

        sys.stdout = out_file

        print(shipment)

        sys.stdout = original_stdout
        out_file.close()
        '''

        print('success')

        '''
        print('----order----')
        order_california = easypost.Order.create(
            to_address = to_address,
            from_address=order_california,
            shipments=[
                shipment
            ]
        )

        print(order_california)
        print('--endorder--')
        '''


        break
     
