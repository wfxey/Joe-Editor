months = {"jan": [10, 20, 30], "feb": [23, 40, 100], "mar": [40, 22, 80], 
          "apr": [12, 3, 88], "may": [50, 90, 102], "jun": [100, 99, 44]}
def calc_months(months = {}):
    d = {}
    for k in months:
        month = sum(months[k])
        d.update({k: month})
    return d
def calc_year(arg):
    total = sum(arg.values())
    print("Total: ${}".format(total))
    return total

d  = calc_months(months)

calc_year(d)