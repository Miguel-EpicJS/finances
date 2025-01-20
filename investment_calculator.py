from os import system, name

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

from math import floor

program_state = -1

historic = []

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def compound_interest():
    clear()
    
    capital = float(input("Initial Capital: "))
    interest = float(input("Interest Rate (12% = 0.12): "))
    time_elapsed = float(input("Elapsed Time According To Interest: "))

    result = capital * (1+interest)**time_elapsed

    print(f"\nFinal Amount: R$ {bcolors.OKGREEN}{round(result, 2)} {bcolors.ENDC}")
    print(f"Profit: R$ {bcolors.OKGREEN}{round(result-capital, 2)} {bcolors.ENDC}")

    historic.append({ "final_amount": result, "profit": result-capital, "interest": interest, "time": time_elapsed })

    input("\n PRESS ENTER TO RETURN ")

def compound_interest_with_monthly_contributions():
    clear()
    
    capital = float(input("Initial Capital: "))
    interest = float(input("Interest Rate Per Month (12% = 0.12): "))
    time_elapsed = float(input("Elapsed Time In Months: "))
    contribution = float(input("Monthly Contribution: "))

    result = capital * (1+interest)**time_elapsed + contribution*( (1 + interest)**time_elapsed - 1 )/ interest

    print(f"\nFinal Amount: R$ {bcolors.OKGREEN}{round(result, 2)} {bcolors.ENDC}")
    print(f"Profit: R$ {bcolors.OKGREEN}{round(result-capital, 2)} {bcolors.ENDC}")

    historic.append({ "final_amount": result, "profit": result-capital, "interest": interest, "time": time_elapsed })

    input("\n PRESS ENTER TO RETURN ")

def reit_simulator():
    clear()

    share_value = float(input("Value per Share: "))
    share_dividend = float(input("Average of Past Dividends: "))
    capital = float(input("Initial Capital: "))
    time_elapsed = int(input("Simulated Time in Months: "))
    contribution = float(input("Monthly Contribution: "))

    amount_of_shares = floor(capital / share_value)
    money = capital - floor(capital / share_value)*share_value

    dividends_history = []
    assets_history = []

    for i in range(time_elapsed):
        money += share_dividend * amount_of_shares + contribution

        dividends_history.append(share_dividend * amount_of_shares)
        
        buy = floor(money / share_value)
        
        amount_of_shares += buy
        money -= buy * share_value

        assets_history.append(money + amount_of_shares * share_value)

    print(f"\nFinal Amount: R$ {bcolors.OKGREEN}{round(money+amount_of_shares*share_value, 2)} {bcolors.ENDC}")
    print(f"Final Dividends: R$ {bcolors.OKGREEN}{round(amount_of_shares*share_dividend, 2)} {bcolors.ENDC}")

    historic.append({ "final_amount":  money+amount_of_shares*share_value, "final_dividends": amount_of_shares*share_dividend, "dividends_history": dividends_history, "assets_history": assets_history})

    input("\n PRESS ENTER TO RETURN ")

def history():
    print(historic)

    input("\n PRESS ENTER TO RETURN ")

while program_state != 0:
    clear()
    print(f"{bcolors.WARNING} ---------- ( 0 ) Exit ---------- {bcolors.ENDC}")
    print(" ---------- ( 1 ) Compound Interest ----------")
    print(" ---------- ( 2 ) Compound Interest With Monthly Contributions ----------")
    print(" ---------- ( 3 ) REIT(FII) Simulator ----------")
    print(" ---------- ( 4 ) History ----------")
    
    try:
        program_state = int(input())
    except:
        program_state = 0

    if program_state == 1:
        compound_interest()
    elif program_state == 2:
        compound_interest_with_monthly_contributions()
    elif program_state == 3:
        reit_simulator()
    elif program_state == 4:
        history()
