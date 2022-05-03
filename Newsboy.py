import scipy.stats as st

cost = float(input("Enter cost: "))
price = float(input("Enter price: "))
salvage = float(input("Enter salvage: "))
mean = float(input("Enter mean: "))
sd = float(input("Enter sd: "))

underage_costs = price - cost
overage_costs = cost - salvage
fq = underage_costs / (underage_costs + overage_costs)
z = st.norm.ppf(fq)
quantity = sd * z + mean

print ("The optimal quantity to order is: {0}".format(round(quantity)))