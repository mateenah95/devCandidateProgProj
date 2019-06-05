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
    zip = '90630',
    country = 'US'
)

origin_ohio = easypost.Address.create(
    street1 = '4720 Poth Rd',
    street2 = '',
    city = 'Whitehall',
    state = 'OH',
    zip = '43213',
    country = 'US'
)


with open('sample-data.csv', 'r') as csv_file:
    csv_data = csv.reader(csv_file)

    for index, csv_line in enumerate(csv_data):
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

        '''
        order_california = easypost.Order.create(
            to_address = to_address,
            from_address = origin_california,
            shipments = [shipment_california]
        )
        '''

        california_rates = []
        ohio_rates = []

        for cali_counter in shipment_california.rates:
            california_rates.append(float(cali_counter.rate))

        for ohio_counter in shipment_ohio.rates:
            ohio_rates.append(float(ohio_counter.rate))

        cheapest_california_rate = min(california_rates)
        index_cheapest_california = california_rates.index(cheapest_california_rate)
        cheapest_carrier_california = shipment_california.rates[index_cheapest_california].carrier
        cheapest_service_california = shipment_california.rates[index_cheapest_california].service

        cheapest_ohio_rate = min(ohio_rates)
        index_cheapest_ohio = ohio_rates.index(cheapest_ohio_rate)
        cheapest_carrier_ohio = shipment_ohio.rates[index_cheapest_ohio].carrier
        cheapest_service_ohio = shipment_ohio.rates[index_cheapest_ohio].service

        print("------------------------")

        '''
        print(index_cheapest_california)
        print(cheapest_california_rate)
        print(cheapest_carrier_california)
        print(cheapest_service_california)

        print(index_cheapest_ohio)
        print(cheapest_ohio_rate)
        print(cheapest_carrier_ohio)
        print(cheapest_service_ohio)
        '''

        if cheapest_carrier_california != cheapest_carrier_ohio:
            print('Diff Carrier')
        
        if cheapest_service_california != cheapest_service_ohio:
            print('Diff Service')


        print("------------------------")

        print('success {}'.format(index))

        if index == 3:
            break
     
