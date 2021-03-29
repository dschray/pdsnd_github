import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filter(initial_question, rerun_text, valid_inputs):
    """
    Helper function to ask for specific inputs

    Args:
        (str) initial_question - The initial question which is asked
        (str) rerun_text - The text that is displayed when the user enters not valid responses
        (list) valid_inputs - The valid inputs that are allowed as an answer to the question
    """

    input_invalid = True
    rerun = False
    while input_invalid:
        if rerun:
            filter = input(rerun_text).lower()
        else:
            filter = input(initial_question).lower()

        if filter in valid_inputs:
            input_invalid = False
        else:
            rerun = True
    return filter


def display_raw_data(df):
    """
    Helper function to display the raw data to the user

    Args:
        (dataframe) df - The pandas dataframe from which the data is displayed
    """

    i = 5
    while True:
        print(df[i-5:i])
        i += 5
        more_data = input('\nWould you like to see the next five rows? Enter "yes" or "no".\n')
        if more_data.lower() != 'yes':
            break


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')

    # get the name of the city to analyze
    city = get_filter('The data of which city do you want to analyze? Chicago, New York City or Washington?\n',
                      'Your input was not recognized. Please enter the city names correctly ("Chicago", "New York City" or "Washington"):\n',
                      ['chicago','new york city','washington'])

    # get the type of filter the user wants to apply
    filter_type = get_filter('Would you like to filter the data by month, day, both or not at all? (Please type "none" for no time filter.)\n',
                      'Your input was not recognized. Please enter your choice correctly ("month", "day", "both" or "none"):\n',
                      ['month','day','both','none'])

    # the default filter value is 'all' -> applies in case filter_type is 'none'
    month = 'all'
    day = 'all'

    if filter_type == 'both':
        month = get_filter('Which month? January, February, March, April, May or June?\n',
                           'Your input was not recognized. Please check the spelling and enter a valid input ("January", "February", "March", "April", "May" or "June"):\n',
                           ['january','february','march','april','may','june'])
        day = get_filter('Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday?\n',
                         'Your input was not recognized. Please check the spelling and enter a valid input ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday" or "Sunday"):\n',
                         ['monday','tuesday','wednesday','thursday','friday','saturday','sunday'])
    elif filter_type == 'month':
        month = get_filter('Which month? January, February, March, April, May or June? ',
                           'Your input was not recognized. Please check the spelling and enter a valid input ("January", "February", "March", "April", "May" or "June"): ',
                           ['january','february','march','april','may','june'])
    elif filter_type == 'day':
        day = get_filter('Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday?\n',
                         'Your input was not recognized. Please check the spelling and enter a valid input ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday" or "Sunday"):\n',
                         ['monday','tuesday','wednesday','thursday','friday','saturday','sunday'])

    print('-'*80)
    print('Filter summary')
    print('-'*14)
    print('City: ' + city.title() + '\nMonth: ' + month.title() + '\nDay: ' + day.title())
    print('-'*80)

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

    print('\n' + '-'*80)
    print('Calculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # find the most common month
    popular_month_int = df['month'].mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = months[popular_month_int - 1].title()

    # find the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most common start hour
    popular_hour = df['hour'].mode()[0]

    # print the results
    print('#'*80)
    print('Most popular month:', popular_month)
    print('Most popular day of the week:', popular_day_of_week)
    print('Most popular start hour:', popular_hour)
    print('#'*80)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\n' + '-'*80)
    print('Calculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # find the most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]

    # find the most commonly used end station
    popular_end_station = df['End Station'].mode()[0]

    # find the most popular trip
    popular_trip = df.groupby(['Start Station','End Station']).size().idxmax()

    # print the results
    print('#'*80)
    print('Most popular start station:', popular_start_station, '(Count:', str(len(df[df['Start Station'] == popular_start_station])) + ')')
    print('Most popular end station:', popular_end_station, '(Count:', str(len(df[df['End Station'] == popular_end_station])) + ')')
    print('Most popular trip:', popular_trip[0], '->', popular_trip[1])
    print('#'*80)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\n' + '-'*80)
    print('Calculating Trip Duration...\n')
    start_time = time.time()

    # calculate the total travel time
    total_travel_time = df['Trip Duration'].sum()

    # calculate the mean travel time
    mean_travel_time = df['Trip Duration'].mean()

    # print the results
    print('#'*80)
    print('Total travel time (h):', total_travel_time / 60 / 60)
    print('Average travel time (min):', mean_travel_time / 60)
    print('#'*80)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # determine the counts of user types
    user_type_counts = df['User Type'].value_counts()

    # determine the gender counts and birth year stats (try/catch for washington data)
    no_data = False
    try:
        gender_counts = df['Gender'].value_counts()
        earliest_birthyear = df['Birth Year'].min()
        recent_birthyear = df['Birth Year'].max()
        common_birtyear = df['Birth Year'].mode()[0]
    except KeyError:
        no_data = True

    # print the results
    print('#'*80)
    print('User type counts:')
    for i, v in user_type_counts.items():
        print(i, v)
    if no_data:
        print('No gender data available.');
        print('No birth year data available.');
    else:
        print('\nGender counts:')
        for i, v in gender_counts.items():
            print(i, v)
        print('\nEarliest year of birth:', int(earliest_birthyear))
        print('Most recent year of birth:', int(recent_birthyear))
        print('Most common year of birth:', int(common_birtyear))

    print('#'*80)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def main():
    while True:
        # Ask the user for the desired filter settings
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # Calculate all metrics and display them (4 subfunctions are used)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Ask the user if he/she wants to see the raw data
        see_raw = input('\nWould you like to see the raw data? Enter "yes" or "no".\n')
        if see_raw.lower() == 'yes':
            display_raw_data(df)

        # Ask the user if he/she wants to restart the process with different filters
        restart = input('\nWould you like to restart? Enter "yes" or "no".\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
