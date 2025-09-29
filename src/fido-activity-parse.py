#! /bin/python
# parse Fidelity activity files from stdin
import click
import re
import sys
import csv


def determine_quarter( date ):
    # format is always mm/dd/yyyy

    date_lookup = {'01':'Q1','02':'Q1','03':'Q1',
                   '04':'Q2','05':'Q2','06':'Q2',
                   '07':'Q3','08':'Q3','09':'Q3',
                   '10':'Q4','11':'Q4','12':'Q4'}
    
    mm=date[0:2]
    if not mm in date_lookup:
        return None
    return( date_lookup[ mm ])

@click.command()
@click.option('--account', help='Account(s) to look for', multiple=True, required=True)
def parse_dividends(account):
    """Total dividends from acccount
    """
    creader = csv.reader(sys.stdin, delimiter=',', quotechar='"')
    dreader = None
    # account dict is a dict of dict of symbols
    account_dict = {}
    for a in account:
        account_dict[a] = {}
    quarter=None

    # read until we get to header row
    for row in creader:
        if len(row) > 0 and row[0] == "Run Date":
            dreader = csv.DictReader( sys.stdin, fieldnames=row, delimiter=',', quotechar='"')
            break
    if not dreader:
        print("*** Can't find a header")
        return 1
    
    # read ledger until it stops listing dates, that's the disclaimers at the end
    for row in dreader:
            row_date = row['Run Date']
            if not re.match(r"\d\d/\d\d/\d\d\d\d", row_date ):
                break

            if row['Account'] in account_dict and row['Action'].startswith("DIVIDEND RECEIVED"):
                row_quarter = determine_quarter( row_date )
                if not row_quarter:
                    print(f"*** Can't parse {row_date}")
                    return 1
                if not quarter:
                    quarter = row_quarter
                else:
                    if quarter != row_quarter:
                        print(f"*** Dates switched quarters in ledger, {row_date} is not in {quarter}")
                        return 1
                symbol_dict = account_dict[row['Account']]
                symbol = row['Symbol']
                amount = float( row['Amount'])
                if not symbol in symbol_dict:
                    symbol_dict[symbol] = 0
                symbol_dict[symbol] = symbol_dict[symbol] + amount 


    # read the ledger, print it out
    for account_name, symbol_dict in account_dict.items():
        for symbol, amount in symbol_dict.items():
            print(f"{quarter}, {account_name}, {symbol}, {amount:.2f}")


# main
if __name__ == '__main__':
    parse_dividends()


