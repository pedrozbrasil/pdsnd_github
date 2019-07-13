#Author: Pedro Paredes Zambrano Brasil
#Latest update: 13-07-2019

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS_DATA = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

DAYS_DATA = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

def get_filters():

    city = str(input('Please provide which city you want to analyse: ')).lower() #it does not matter if user enter it captilized or not, code corrects
    while (city in CITY_DATA.keys()) == False:
        city = str(input('Please provide which city you want to analyse: ')).lower()
    print('Sounds good! Let\'s analyse {} data.'.format(city.title()))

    while True: #while loop ensures user will provide the right input
        month = str(input('Please provide the month to filter by, or "all" to apply no month filter: ')).lower()
        if month in MONTHS_DATA:
            break

    while True:
        day = str(input('Please provide the day of week to filter by, or "all" to apply no day filter: ')).lower()
        if day in DAYS_DATA:
            break



    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Let\'s explore some US bikeshare data!')


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
    df['day_of_week'] = df['Start Time'].dt.weekday_name

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
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', popular_month)

    popular_week_day = df['day_of_week'].mode()[0]
    print('Most Popular Day of the Week:', popular_week_day)

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['hour'] = df['Start Time'].dt.hour

    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station)
    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    popular_combination = df[['Start Station', 'End Station']].mode().loc[0]
    print('Most popular combination :', popular_combination[0], 'and', popular_combination[-1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = df['Trip Duration'].sum()
    print("Total travel time :", total_time)

    # TO DO: display mean travel time
    avg_time = df['Trip Duration'].mean()
    print("Mean travel time :", avg_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city): #As Washington has less columns, it was added another variable to allow the code to adapt without breaking
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    user_type = df['User Type'].value_counts()
    print('Counts of user types:\n', user_type)


    if city != 'washington': #As there is no data related to gender for DC, it prevents the code from crashing
        gender = df['Gender'].value_counts()
        print('Counts of gender:\n', gender)
    else:
        print('No gender data available for Washington D.C') #way of indicating to the user that this type of data is not available to DC


    if city != 'washington':
        earliest_birth= df['Birth Year'].min()
        print('The earliest year of birth:', str(int(earliest_birth))) #converting year to integer and string later to take the float part

        latest_birth= df['Birth Year'].max()
        print('The latest year of birth:', str(int(latest_birth)))

        popular_birth= df['Birth Year'].mode()[0]
        print('The most common year of birth:', str(int(popular_birth)))

        print("\nThis took %s seconds." % (time.time() - start_time))
    else:
        print('No user birth data available for Washington D.C')

    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
