import time
import calendar
import pandas as pd
import numpy as np



CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }



def get_filters():
    city = None
    month = None
    day = None
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("\nPlease enter the name of the city you would like to pull the data from.\nThe only options currently available are: Chicago, New York City or Washington.\n").lower()
    while True:
        if city in CITY_DATA.keys():
            print('you have selected {}!\n'.format(city).title())
            break
        else:
            city = input("\nThe only options are Chicago, New York City or Washington.\nPlease try entering the city again\n").lower()
            continue
    # get user input for month (all, january, february, ... , june)
    month = input("\nNow enter the month you would like see the data for.  The only options currently available are January, February, March, April, May, June or All.\n").lower()
    while True:
        if month in ['january', 'february', 'march', 'april', 'may', 'june' ,'all']:
            print('you have selected {}!\n'.format(month).title())
            break
        else:
            month = input("\nThere was an error! Try entering the month again.\nPossible options are January, February, March, April, May, June or All.\n").lower()
            continue
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("\nLast, please enter the day of the week that you would to see the data for.\nOptions are Monday, Tuesday, ... Sunday or All.\n").lower ()
    while True:
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            print('you have selected {}!\n'.format(day).title())
            break
        else:
            day = input("\nThere was an error! Try entering the day of the week again.\nPossible options are monday, tuesday, wednesday, thursday, friday, saturday, sunday or all.\nPlease try entering the day of the week again\n").lower()
            continue
    print('-*_*'*40)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns also create columns for route
    df['month_int'] = df['Start Time'].dt.month
    df['Month'] = df['month_int'].apply(lambda x: calendar.month_name[x])
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[(df.month_int == month)]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    if month != 'all':
        print('Most Frequent Start Month: N/A, only {} selected.'.format(month).title())
    else:
        popular_month = df['Month'].mode()[0]
        print('Most Frequent Start Month:', popular_month)
    # display the most common day of week
    if day != 'all':
        print('Most Frequent Start Day of Week: N/A, only {} selected.'.format(day).title())
    else:
        popular_day = df['day_of_week'].mode()[0]
        print('Most Frequent Start Day of Week:', popular_day)
    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour: {}:00'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-*_*'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # display most commonly used start station
    popular_sstation = df['Start Station'].mode()[0]
    print('Most Frequent Start Station:', popular_sstation)
    # display most commonly used end station
    popular_estation = df['End Station'].mode()[0]
    print('Most Frequent End Station:', popular_estation)
    # display most frequent combination of start station and end station trip
    df['Trip'] = 'Start at ' + df['Start Station'] + ' and travel to ' + df['End Station']
    popular_route = df['Trip'].mode()[0]
    print('Most Frequent Trip:', popular_route)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-*_*'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print('Total Travel Time:', total_travel)
    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print('Average Travel Time:', mean_travel)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-*_*'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    print('\nFirst is the count of the user types...\n')
    user_type_count = df['User Type'].value_counts()
    i = 0
    for i in range(len(user_type_count)):
        if i < len(user_type_count):
            print('The total trips taken by the user type "{}" during this period was {}.'.format(user_type_count.index[i],user_type_count.values[i]))
            i+1
    # Display counts of gender
    print('\nNext is the count of the gender types...\n')
    if 'Gender' in df:
	    gender_count = df['Gender'].value_counts()
	    i = 0
	    for i in range(len(gender_count)):
	        if i < len(gender_count):
	            print('The total trips taken the gender type "{}" during this period was {}.'.format(gender_count.index[i],gender_count.values[i]))
	            i+1
    else:
    	print('\nNo Gender Data Available.\n')
    # Display earliest, most recent, and most common year of birth
    print('\nLast is the earliest, most recent and most common year of birth of the users...\n')
    if 'Birth Year' in df:
	    earliest_birth = df['Birth Year'].min()
	    print('The earliest birth year in this user group:', int(earliest_birth))
	    most_recent_birth = df['Birth Year'].max()
	    print('The most recent birth year in this user group:', int(most_recent_birth))
	    most_common_birth = df['Birth Year'].mode()
	    print('The most common birth year in this user group:', int(most_common_birth))
    else:
        print('\nNo Birth Year Data Available.\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-*_*'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        #ask if the user wants to see 5 rows of data
        show_code = input('\nWould you like to see the data? Enter yes or no.\n')
        i = 0
        while show_code.lower() == 'yes':
            print(df.iloc[[i,i+1,i+2,i+3,i+4]])
            i=i+5
            show_code = input('\nWould you like to see 5 more lines? Enter yes or no.\n')
        #ask if the user wants to restart the code or exit
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

main()