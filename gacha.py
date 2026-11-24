import random
import statistics
import matplotlib.pyplot as plt
import math

##############################################

banner_rate = 0.7          # 0.7% rate up
general = 112              # off non limited 3* units

simulations = 10000      # number of simulations

hist_chart = False          # generates histograms
pie_chart = False           # generates pie chart

##############################################

count = 0
banner_char = 0

old_pulls = []
old_spending = []
leftover_pity = []
new_pulls = []
new_spending = []
new_freebies = []

banner_chance=banner_rate+((3-banner_rate)/(general+1))

old_stats ={"old200": 0,
            "old400": 0,
            "1spark": 0,
            "%100": 0,
            "%200": 0,
            "%300": 0,
            "%400": 0,
            "offrate": 0}

new_stats ={"new200": 0,
            "new400": 0,
            "new240": 0,
            "1 50/50 reached": 0,
            "1 50/50 success": 0,
            "1 pity reached": 0,
            "2 50/50 reached": 0,
            "2 50/50 success": 0,
            "2 pity reached": 0,
            "%100": 0,
            "%200": 0,
            "%300": 0,
            "%400": 0,
            "offrate": 0,
            "rebate pulls": 0}

# Simulates rolling in old system
# Will perform up to 400 rolls
# If 1 character before 200 pulls, pull until 2 characters or spark at 200
# If 1 character after 200 pulls, sparks second character and exits
# Sparks both at 400 pulls

def old_sim ():
    count = 0
    charge = 0
    banner_char = 0

    while banner_char == 0:
        g=random.random()*100
        if g <= banner_chance:
            banner_char = 1
            if g>banner_rate:
                old_stats["offrate"]+=1
        charge+=1
        count+=1
        if charge == 400:
            banner_char = 2
            charge=0
            old_stats["1spark"]+=2
  
    if  charge>=200:
        banner_char = 2
        charge -= 200
        old_stats["1spark"]+=1
    
    while banner_char == 1:
        g=random.random()*100
        if g <= banner_rate:
            banner_char = 2
        charge+=1
        count+=1
        if  charge==200 and banner_char == 1:
            banner_char = 2
            charge = 0
            old_stats["1spark"]+=1
    if count <= 200:
        old_stats["old200"]+=1
    if count == 400:
        old_stats["old400"]+=1
    
    old_pulls.append(count)
    old_spending.append(count*120)
    leftover_pity.append(charge)


# Simulates rolling in new system
# Will perform up to 400 rolls
# Charge doesnt reset for off rate
# Sparks both at 400 pulls
def new_sim ():
    freebies = 0
    count = 0
    banner_char = 0
    charge = 0
    max_charge = 0
    spending = 0
    rebate = 0

    while banner_char == 0:

        charge+=1
        max_charge += 1
        g=random.random()*100

        if charge == 100:
            new_stats["1 50/50 reached"] += 1
            if g > 50:
                banner_char = 1
                charge = 0
                new_stats["1 50/50 success"] += 1
            if g <= 50/(general+1):
                banner_char = 1
                new_stats["offrate"] += 1
        elif charge == 200:
            banner_char = 1
            charge = 0
            new_stats["1 pity reached"] +=1
        elif g <= banner_chance:
            banner_char = 1
            if g>banner_rate:
                new_stats["offrate"]+=1
            else:
                charge = 0

        count+=1
        if rebate == 0:
            spending += 120
        else:
            rebate -= 1
            freebies += 1
        if max_charge in [70,130,150,170,270,330,350,370]:
            rebate = 10

    while banner_char == 1:
        charge+=1
        max_charge += 1
        g=random.random()*100
        if charge == 100:
            new_stats["2 50/50 reached"] += 1
            if random.randint(1,2) == 2:
                banner_char = 2
                new_stats["2 50/50 success"] += 1
        elif charge == 200:
            banner_char = 2
        elif g <= banner_chance:
            banner_char = 2
        count+=1
        if rebate == 0:
            spending += 120
        else:
            rebate -= 1
            freebies += 1
        if max_charge in [70,130,150,170,270,330,350,370]:
            rebate = 10
    charge = 0

    if count == 400:
        new_stats["new400"]+=1
    if count <= 200:
        new_stats["new200"]+=1
    if count <= 240:
            new_stats["new240"]+=1
    
    new_pulls.append(count)
    new_spending.append(spending)
    new_freebies.append(freebies)

#runs simulations
for i in range(simulations):
    old_sim()
    new_sim()

#print(old_pulls)
#print(new_pulls)

old_avg = sum(old_pulls)/len(old_pulls)
new_avg = sum(new_pulls)/len(new_pulls)
free_avg = sum(new_freebies)/len(new_freebies)

print()
print ("Old Average = " + str(old_avg))
print ("New Average = " + str(new_avg) + ",  of which " + str(round(new_avg-free_avg, 4)) + " were paid and " + str(free_avg) + " were freebies")

old_median = statistics.median(old_pulls)
new_median = statistics.median(new_pulls)

print()
print ("Old median = " + str(old_median))
print ("New median = " + str(new_median))

print()
print("Pulled to 200 or less on old system "+str(old_stats["old200"])+" times ("+str(100*old_stats["old200"]/simulations)+"%"+" of pulls)")
print("Pulled to 240 or less on new system "+str(new_stats["new240"])+" times ("+str(100*new_stats["new240"]/simulations)+"%"+" of pulls)")

print()
print("Pulled to exactly 200 on old system "+str(old_stats["1spark"])+" times ("+str(100*old_stats["1spark"]/simulations)+"%"+" of pulls)")

print()

print("Pulled offrates on old system "+str(old_stats["offrate"])+" times")
print("Leftover pity on old system "+str(sum(leftover_pity))+", average " +str(round(sum(leftover_pity)/simulations))+" per session")

print()
print("Reached the first 50/50 "+str(new_stats["1 50/50 reached"])+" times ("+str(100*new_stats["1 50/50 reached"]/simulations)+"%"+" of pulls), and was successful "+str(new_stats["1 50/50 success"])+" times ("+str(100*new_stats["1 50/50 success"]/simulations)+"%"+" of pulls)")
print("Reached the first pity "+str(new_stats["1 pity reached"])+" times ("+str(100*new_stats["1 pity reached"]/simulations)+"%"+" of pulls)")
print("Reached the second 50/50 "+str(new_stats["2 50/50 reached"])+" times ("+str(100*new_stats["2 50/50 reached"]/simulations)+"%"+" of pulls), and was successful "+str(new_stats["2 50/50 success"])+" times ("+str(100*new_stats["2 50/50 success"]/simulations)+"%"+" of pulls)")
print("Reached the second pity "+str(new_stats["new400"])+" times ("+str(100*new_stats["new400"]/simulations)+"%"+" of pulls)")
print("Pulled offrates on new system "+str(new_stats["offrate"])+" times")

print()
print("Pulled to 400 on old system "+str(old_stats["old400"])+" times ("+str(100*old_stats["old400"]/simulations)+"%"+" of pulls)")
print("Pulled to 400 on new system "+str(new_stats["new400"])+" times ("+str(100*new_stats["new400"]/simulations)+"%"+" of pulls)")

#print()
#print("Old highest: "+str(max(old_pulls))+" pulls")
#print("New highest: "+str(max(new_pulls))+" pulls")

print()

label = []
for l in range (40):
    label.append(str(l*10)+" - "+str((l+1)*10))

old_hist = [0]*40
for t in range(simulations):
    old_hist[math.ceil(old_pulls[t]/10)-1] += 1

new_hist = [0]*40
for t in range(simulations):
    new_hist[math.ceil(new_pulls[t]/10)-1] += 1

old_stats["%100"] = sum(old_hist[0:10])/simulations
old_stats["%200"] = sum(old_hist[10:20])/simulations
old_stats["%300"] = sum(old_hist[20:30])/simulations
old_stats["%400"] = sum(old_hist[30:40])/simulations

old_pie = [old_stats["%100"], old_stats["%200"], old_stats["%300"], old_stats["%400"]]

new_stats["%100"] = sum(new_hist[0:10])/simulations
new_stats["%200"] = sum(new_hist[10:20])/simulations
new_stats["%300"] = sum(new_hist[20:30])/simulations
new_stats["%400"] = sum(new_hist[30:40])/simulations

new_pie = [new_stats["%100"], new_stats["%200"], new_stats["%300"], new_stats["%400"]]

def create_histogram(hist, label, color, title, xtitle, ytitle):
    fig, ax = plt.subplots()
    ax.bar(label, hist, color=color, width=0.35)
    ax.set_title(title, loc="center")
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    ax.tick_params(axis='x', labelrotation=90)
    rects = ax.patches
    for rect, label in zip(rects, hist):
        height = rect.get_height()
        ax.text(
            rect.get_x() + rect.get_width() / 2, height + 1, label, ha="center", va="bottom"
        )
    plt.show()

def create_pie(stats, title):
    pie_labels = '1-100 pulls', '101-200 pulls', '201-300 pulls', '301-400 pulls'
    sizes = stats
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=pie_labels, autopct='%1.1f%%')
    ax.set_title(title, loc="center")
    plt.show()

if (hist_chart):
    create_histogram(old_hist, label, "blue", "Successful exits at every 10 pulls on old system", "Total pulls", "Successful exits")
    create_histogram(new_hist, label, "orange", "Successful exits at every 10 pulls on new system", "Total pulls", "Successful exits")

if (pie_chart):
    create_pie(old_pie, "Successful exits at every 100 pulls on old system")
    create_pie(new_pie, "Successful exits at every 100 pulls on new system")

print("Average spending on the old system: "+str(round(sum(old_spending)/simulations))+" pyros")
print("Average spending on the new system: "+str(round(sum(new_spending)/simulations))+" pyros")

old_percentiles = statistics.quantiles(old_pulls, n=100)
new_percentiles = statistics.quantiles(new_pulls, n=100)

print()
print("Percentile distribution of total pulls")
print("----------------------------------------------------")
print("            p10  | p50   | p90   | p95   | p99")
print("Old system: "+str(old_percentiles[9])+" | "+str(old_percentiles[49])+" | "+str(old_percentiles[89])+" | "+str(old_percentiles[94])+" | "+str(old_percentiles[98]))
print("New system: "+str(new_percentiles[9])+" | "+str(new_percentiles[49])+" | "+str(new_percentiles[89])+" | "+str(new_percentiles[94])+" | "+str(new_percentiles[98]))
print("----------------------------------------------------")

old_win = 0
new_win = 0
tie_win = 0

for w in range(simulations):
    if old_spending[w] > new_spending[w]:
        new_win+=1
    elif old_spending[w] < new_spending[w]:
        old_win+=1
    elif old_spending[w] == new_spending[w]:
        tie_win+=1

print()

print("Old system performed better "+str(old_win)+" times")
print("New system performed better "+str(new_win)+" times")
print("Systems tied "+str(tie_win)+" times")

print()

bar_data = {"Successful exits on old system" : old_hist,
            "Successful exits on new system" : new_hist}

fig, ax = plt.subplots()
rects = ax.grouped_bar(bar_data, tick_labels=label, group_spacing=1)
ax.set_title("Successful exits at every 10 pulls on old system (blue) and new system (orange)", loc="center")
plt.xlabel("Total pulls")
plt.ylabel("Successful exits")
ax.legend(loc='upper left', ncols=2)
ax.tick_params(axis='x', labelrotation=90)
for container in rects.bar_containers:
    ax.bar_label(container, padding=3)
plt.show()