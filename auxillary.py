'''
Auxillary functions
'''
import pandas as pd
import io_data as iod

def choose_random(meals, rank=False, times=False, last_made=False, TA=None, k=1):
    '''
    Changes to make:
    1. test time stamping

    makes either a fully (pseudo) random choice from all meal options
        or a weighted choice based on rank.
    Future:
        1. Adjust weights according to times made.
        2. Make choice by ease
        3. Give k-choices ranked by ease and/or rank
        4. make choice by kosher type
        5. if last_made don't make choice made in last 5 days or if last_made==int then that amount of days
    meals     ::: DataFrame with meal information
    rank      ::: if True gives weights to meals based on rank
    last_made ::: *NOT IMPLEMENTED* should take into account when last made, maybe combine with times?
    TA        ::: True - choose only from takeawy, False - choose only from homecooking, None - anything may come
    '''
    use_rank = None
    if rank == True:
        use_rank = choice["Rank"]
    if TA == "True": 
        choice = meals[meals["TA"] == 1].sample(n=k, weights=use_rank)
    if TA == "False":
        choice = meals[meals["TA"] == 0].sample(n=k, weights=use_rank)
    else:
        choice = meals.sample(n=k, weights=use_rank)
    # check if user wants to make meal and if yes log the meal.
    print(choice["Name"].iloc[0])
    make_it = input("Are you going to make this meal? (y/n)")
    while True:
        if make_it.lower() == "y":
            meals.loc[choice.index[0],"times_made"] += 1
            meals.loc[choice.index[0],"Timestamp"] = pd.Timestamp.now()
            iod.save_data(meals,filename="meal_list.csv")
            iod.write_to_log(choice) 
            print("meal logged.")
            break
        elif make_it.lower() == "n":
            print("meal not logged.")
            break
        else:
            print("Please enter a valid answer.")
            make_it = input("Are you going to make this meal? (y/n)")
    return choice["Name"].iloc[0]

def is_too_late_to_cook(cutoff = 20):
    '''
    Checks actual time and returns if choose_random should skip ideas with long preparation time.
        After 20:00 only short and medium durations will be considered.
    1. Needs cooking duration feature implemnted.
    2. Option: ask user how long does he plan to prepare the meal
    
    IMPORTANT: only takes into account that the time is less than 20:00, if you start cooking after midnight this function will fail to work properly.
    '''
    hour = pd.Timestamp.now().hour
    if hour < cutoff:
        return False
    else:
        return True

def reboot_time_timestamps(data):
    '''
    Resets all times made to 0 and removes all time stamps.
    This is currently designed only testing and developing.
    '''
    while True:
        just_checking = input("Are you sure you want to reset *ALL* timestamps and all times_made? (y/n)")
        if just_checking.lower() == "n":
            print("data was not reset")
            return 0
        elif just_checking.lower() == "y":
            data["Timestamp"] = "NaN"
            data["times_made"] = 0
            iod.save_data(data)
            print("Data was reset and saved")
            return 0

if __name__ == "__main__":
    FILENAME = "meal_list.csv"
    data = pd.read_csv(FILENAME,index_col=0)
    print(data.head(n=5))
    reboot_time_timestamps(data)
    print(data.head(n=5))
    #choose_random(data, rank=False, times=False)
    #choose_TA(data)
    #data = add_meal(data,["Pasta tomato","Stir Fried Veggies Frozen Bag"],[1,1],[4,4],[3,7])
    #save_data(data)
    #print(data)

