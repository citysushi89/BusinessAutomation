"""
main.py accesses a csv pulled from the shopify order page, and returns information required for filing sales tax in NC
data and output hidden for privacy
"""

# Get Access to data in folder
import csv
from datetime import datetime

COUNITES_W_TRANSIT_TAX_2_BASE = ['Mecklenburg', 'Wake']
COUNITES_W_TRANSIT_TAX_225_BASE = ['Durham','Orange']
FILENAME = 'orders_export_1.csv'

orders = []
with open(f'data\{FILENAME}', mode='r') as f:
    csvf = csv.reader(f)
    for lines in csvf:
        orders.append(lines)

# General setup for loop
orders_w_taxes = []
nc_gross_receipts = 0
not_nc_gross_receipts = 0

# Specific categories
gen_state_rate_due = 0
county_2_per = 0
county_2_p_25_per = 0
transit_5_per = 0

counties_to_pay_in = []

for order in orders[1:]:
    tax_col = order[10]
    # Find just the orders where taxes were collected by shopify
    if tax_col != '' and tax_col != '0.00' and tax_col != 'Taxes':
        single_county_payment = []

        # Line 1 - takes the subtotal 
        nc_gross_receipts += float(order[8])

        county_name = order[58].split(' ')[0]
        county_rate = order[58].split(' ')[3]
        county_cost = order[59]

        if county_name == "North":
            county_name = order[56].split(' ')[0]
            county_rate = order[56].split(' ')[3]
            county_cost = order[57]
            gen_state_rate_due += float(order[59])

        # Add to general state rate if county and state were not flipped
        else:
            gen_state_rate_due += float(order[57])

        county_rate = county_rate.replace('%', '')

        if county_name in COUNITES_W_TRANSIT_TAX_225_BASE:
            county_cost_separate_from_transit = float(county_cost)
            # Calculate the separate county and transit rate
            # .8182 comes from 2.25 being 81.82 % of 2.75
            county_cost_alone = county_cost_separate_from_transit * .8182
            trans_cost_alone = county_cost_separate_from_transit * .1818
            county_2_p_25_per += float(county_cost_alone)
            transit_5_per += float(trans_cost_alone)
        elif county_name in COUNITES_W_TRANSIT_TAX_2_BASE:
            # Need to add to 2 AND Transit rate
            county_cost_separate_from_transit = float(county_cost)
            # Calculate the separate county and transit rate
            # .80 comes from 2 being 80% of 2.5
            county_cost_alone = county_cost_separate_from_transit * .80
            trans_cost_alone = county_cost_separate_from_transit * .20
            county_cost_alone_rounded = round(float(county_cost_alone), 2)
            county_2_per += county_cost_alone_rounded
            trans_cost_alone_rounded = round(float(trans_cost_alone), 2)
            transit_5_per += trans_cost_alone_rounded
        
        elif county_rate == '2.25':
            county_cost_rounded = round(float(county_cost), 2)
            county_2_p_25_per += county_cost_rounded
        elif county_rate == '2':
            county_cost_rounded = round(float(county_cost), 2)
            county_2_per += county_cost_rounded

        already_logged_county = False
        index = 0
        for item in counties_to_pay_in:
            if item[0] == county_name:
                already_logged_county = True
                break
            index += 1

        # If the county is already in the list to pay for
        if already_logged_county:   
            # Try to append with a transit tax
            try:
                total_county_cost_alone = float(counties_to_pay_in[index][1]) + float(county_cost_alone)
                total_county_cost_alone = round(total_county_cost_alone, 2)
                counties_to_pay_in[index][1] = total_county_cost_alone  
                # single_county_payment.append(total_county_cost_alone)
                total_trans_cost_alone = float(counties_to_pay_in[index][2]) + float(trans_cost_alone)
                total_trans_cost_alone = round(total_trans_cost_alone, 2)
                counties_to_pay_in[index][2] = total_trans_cost_alone  
                # single_county_payment.append(total_trans_cost_alone)
            except IndexError:
                total_county_cost = float(counties_to_pay_in[index][1]) + float(county_cost)
                total_county_cost = round(total_county_cost, 2)
                counties_to_pay_in[index][1] = total_county_cost
                # counties_to_pay_in.append(total_county_cost)
                pass

        # If not already in the list
        else:
            single_county_payment.append(county_name)
            try:
                county_cost_alone = round(county_cost_alone, 2)
                single_county_payment.append(county_cost_alone)
                trans_cost_alone = round(trans_cost_alone, 2)
                single_county_payment.append(trans_cost_alone)
            except NameError:
                county_cost = round(float(county_cost), 2)
                single_county_payment.append(county_cost)
            counties_to_pay_in.append(single_county_payment)
        print(f'counties to pay in: {counties_to_pay_in}')

    # Receipts not subject to NC taxes
    else:
        if order[8] == '':
            pass
        else:
            # Line 3
            not_nc_gross_receipts += float(order[8])

total = gen_state_rate_due + county_2_per + county_2_p_25_per + transit_5_per

now = datetime.now()
date = now.strftime('%d%b%Y')

with open(f'output/sales_tax_report_{date}_.csv', mode='w') as file:
    file.writelines(f'PAGE 1\n'
    f'nc receipts taxable (line 1): {nc_gross_receipts}\n'
    f'not taxable (line 3): {not_nc_gross_receipts}\n'
    f'General state rate due (line 4): {gen_state_rate_due}\n'
    f'General state rate due (line 4): {gen_state_rate_due}\n'
    f'2% county rate to be paid: {county_2_per}\n'
    f'2.25% county rate to be paid: {county_2_p_25_per}\n'
    f'.5% transit rate to be paid: {transit_5_per}\n'
    f'Total this quarter: ${total}\n'
    '\n'
    '\n'
    )

    file.writelines(f'PAGE 2\n'
    f'{counties_to_pay_in}'
    )
