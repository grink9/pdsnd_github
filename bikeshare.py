import time
import pandas as pd
import numpy as np
from collections import Counter

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = 0
    while city not in CITY_DATA:
        city = input('Which city would you like to investigate - Chicago, New York City or Washington? ').lower()

    # get user input for month (all, january, february, ... , june)
    month = 0
    month_list = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while month not in month_list:
            month = input('Which month would you like to search - January, February, March, April, May, June or All? ').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = 0
    days_of_week_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while day not in days_of_week_list:
        day = input('Let\'s pick a day of the week to examine - Please enter a day or all: ').lower()

    print('-'*40)
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

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day)
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('Most common month of travel - ', common_month)

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most common day of travel - ', common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_start = df['hour'].mode()[0]
    print('Most common starting hour - ', common_start)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # d isplay most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('Most common start station - ', start_station)

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('Most common end station - ', end_station)

    # display most frequent combination of start station and end station trip
    df.insert(5, 'Station Trip', df['Start Station'])
    df['Station Trip'] += ' to ' + df['End Station']
    station_trip = df['Station Trip'].mode()[0]
    print('Most frequent station trip - ', station_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print('\nTotal travel time = ', total_travel)

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print('Average travel time = ', mean_travel)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].values
    user_types = Counter(user_types)
    user_types = pd.Series(user_types)
    print('Here are the user types:\n', user_types)

    # Display counts of gender
    if 'Gender' not in df.columns:
        return
    gender = df['Gender'].values
    gender = Counter(gender)
    gender = pd.Series(gender)
    print('Breakdown by gender:\n', gender)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' not in df.columns:
        return
    earliest_birth = df['Birth Year'].max()
    recent_birth = df['Birth Year'].min()
    common_birth = df['Birth Year'].mode()
    print('\nHere is a look at some age information!\n')
    print('Earliest birth year: ', earliest_birth)
    print('Most recent birth year: ', recent_birth)
    print('Most common birth year: ', common_birth)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def data_display(df):
    '''Displays raw data - five lines at a time - as long as user requests'''
    display = input('Would you like to see some raw data?  Yes or No. ').lower()
    x = 0
    while display == 'yes':
        print(df.iloc[x:x+5, 3:10])
        display = input('\nWould you like to see 5 more rows?  Yes or No. \n').lower()
        x += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data_display(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
