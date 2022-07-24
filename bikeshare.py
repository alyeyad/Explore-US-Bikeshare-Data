import time
import pandas as pd

pd.set_option("Display.max_columns",20)

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    #asking the user for input
    city = input("Would you like to explore Chicago, New York City, or Washington? ").lower()
    #validating input
    while city != 'chicago' and city != 'washington' and city != 'new york city':
        city = input("Invalid City, please re-enter (Chicago, New York City, Washington) ").lower()

    #month and day are set to all by default, can be modified if user does not choose none
    month='all'
    day='all'

    #asking user for preferred method of filtering
    filter_choice=input("How would you like to filter data? (Month, Day, All, None) ").lower()
    #validating filter preference input
    while filter_choice not in ['month', 'day', 'all', 'none']:
        filter_choice=input("Invalid Filtering Choice! Please Enter (Month, Day, All , None) ").lower()

    #filtering by month (case month or all)
    if filter_choice=='month' or filter_choice=='all':
        month = input('Which month would you like to filter by? (January, February, March, April, May, June, All) ').lower()
        #validating month input
        while month not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            month = input("Invalid Month, please re-enter (January, February, March, April, May, June, All): ").lower()

    # filtering by day (case day or all)
    if filter_choice=='day' or filter_choice=='all':
        day = input('Which day would you like to filter by? (Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, All): ').lower()
        while day not in ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'all']:
             day = input("Invalid day, please re-enter (Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, All): ").lower()

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #loading the appropriate csv file
    df = pd.read_csv(CITY_DATA[city])
    #converting start time to the datetime datatype
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #extracting months for filtering
    df['month'] = df['Start Time'].dt.month
    #extracting days for filtering
    df['day_of_week'] = df['Start Time'].dt.day_name()
    #filtering data by appropriate month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    #filtering data by appropriate day
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #note: all common measures are done using mode function
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    common_month = df['month'].mode()[0]
    print("The most common month is:", months[common_month - 1].title())

    #most common day of week
    common_day = df['day_of_week'].mode()[0]
    print("The most common day is:", common_day)
    #most common start hour
    common_hour = df['Start Time'].dt.hour.mode()[0]
    print("The most common Starting hour is:", common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trips...\n')
    start_time = time.time()

    #most common starting station
    print("The most commonly used start station is:", df['Start Station'].mode()[0])

    #most common end station
    print("The most commonly used end station is:", df['End Station'].mode()[0])

    """
    Most common combination of start and end station:
    -grouping data and counting the count of end stations against every start station
    -then inputting these counts into a dictionary and reversing it to navigate using counts
    -and displaying the station associated with the max count
    
    *Note: 
    -This was my initial solution, I'm aware that it is somehow complex,
     I saw another solution in the code for the walkthrough webinar
     but the instructor did not mean to show it to us, so I did not use it.
    """
    start_end_group = df.groupby(['Start Station'])['End Station'].value_counts()
    start_end_dict = dict(start_end_group)
    start_end_dict = ((val, key) for (key, val) in start_end_dict.items())
    start_end_tuple = max(start_end_dict)[1]
    print("The Most Frequent Combination of Start Station and End Station is: ({} , {})".format(start_end_tuple[0],
                                                                                                start_end_tuple[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #total trip duration (summing the trip duration column)
    total_travel_time = df['Trip Duration'].sum()
    print("Total Travel Time:", total_travel_time)

    #mean travel time using mean function
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean Travel Time:", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #counting user types seperately for simplicity
    type_counts = df['User Type'].value_counts()

    print("Type Counts:")
    for i in type_counts.index:
        print(i, ':', type_counts[i], '\n')
    #Note that Washington has no gender information or date of birth
    if city != 'washington':
        gender_counts = df['Gender'].value_counts()
        print("Gender Counts:")
        for i in gender_counts.index:
            print(i, ':', gender_counts[i], '\n')

        #information about year of birth
        print("Earliest Year of Birth:", int(df['Birth Year'].min()))
        print("Most Recent Year of Birth:", int(df['Birth Year'].max()))
        print("Most Common Year of Birth:", int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def raw_data(df):
    """
        A function that asks the user if they want to see raw rows of data
        and displays them, 5 at a time
        Args:
            (Pandas.DataFrame) df: the dataframe of filtered data to display from
        No Returns
        """
    #starting display at the first row
    cnt=0
    #the last possible index (number of rows)
    last = len(df.index)
    #input: yes or no
    rdata_response=input("Would you like to see raw data? (yes, no): ")

    while rdata_response.lower()=="yes":
        #printing 5 rows of data
        #note that if the number of rows left is less than 5, they should be displayed instead
        print(df.iloc[cnt:min(cnt+5,last)])
        cnt += 5
        #stopping the display if all rows are displayed
        if cnt>=last:
            print("End of Data")
            break
        rdata_response=input("Would you like to see some more data?")
    print('-' * 40)

def main():
    print("Explore US Bikeshare Data Project")
    print("Designed by Aly Eyad\n")
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("Thank you for using our Service!")
            break


if __name__ == "__main__":
    main()
