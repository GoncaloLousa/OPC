import math
import scipy.stats as st

cost = 6
order_cost = 15
int_rate = 0.3
lead_time = 3.5
mean = 28
sd = 8
normal_time = 1
p = 10

if normal_time != lead_time:
    new_mean = mean * (normal_time / (normal_time / lead_time))
    new_sd = math.sqrt((sd * sd) * (normal_time / (normal_time / lead_time)))

else:
    new_mean = mean
    new_sd = sd

tau = lead_time / 12
gama = new_mean / tau
holding_cost = int_rate * cost

q_zero = math.sqrt((2 * order_cost * gama) / holding_cost)
f_zero = 1 - ((q_zero * holding_cost) / (p * gama))
z_zero = st.norm.ppf(f_zero)
r_zero = new_sd * z_zero + new_mean
Lz_zero = st.norm.pdf(z_zero) - z_zero * (1 - st.norm.cdf(z_zero))
n_rzero = new_sd * Lz_zero

n_rnew = n_rzero
old_q = q_zero
new_q = 0

while abs(new_q - old_q) >= 2:
    n_rold = n_rnew
    old_q = new_q
    new_q = math.sqrt((2 * gama * (order_cost + p * n_rold)) / holding_cost)
    f_new = 1 - ((new_q * holding_cost) / (p * gama))
    z_new = st.norm.ppf(f_new)
    r_new = new_sd * z_new + new_mean
    Lz_new = st.norm.pdf(z_new) - z_new * (1 - st.norm.cdf(z_new))
    n_rnew = new_sd * Lz_new

    if abs(new_q - old_q) <= 2:
        break

print("This is the optimal order quantity: {0}".format(round(new_q)))
print("This is the optimal reorder point: {0}".format(round(r_new)))