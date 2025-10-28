import pm4py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def read_csv(file_path, delimiter=',', datetime_column=None, datetime_format=None):
    df = pd.read_csv(file_path, delimiter=delimiter)
    if datetime_column:
        df[datetime_column] = pd.to_datetime(df[datetime_column], format=datetime_format)
    return df

def convert_to_event_log(df, case_id_col, activity_col, timestamp_col):
    event_log = pm4py.format_dataframe(df, case_id=case_id_col, activity_key=activity_col, timestamp_key=timestamp_col)
    event_log = pm4py.convert_to_event_log(event_log)
    return event_log

def export_event_log(event_log, output_path, format='xes'):
    if format == 'xes':
        pm4py.write_xes(event_log, output_path)
    elif format == 'csv':
        pm4py.write_csv(event_log, output_path)
    else:
        raise ValueError("Unsupported format. Use 'xes' or 'csv'.")

def analyze_event_log(event_log):
    print("Analyzing event log...")
    print(f"Start activities: {pm4py.get_start_activities(event_log)}")
    print(f"End activities: {pm4py.get_end_activities(event_log)}")

    print(f"All case durations: {pm4py.get_all_case_durations(event_log)}")
    print(f"Duration of a case '1': {pm4py.get_case_duration(event_log,'1')}")

    print(f"Rework cases: {pm4py.get_rework_cases_per_activity(event_log)}")

def show_dotted_chart(event_log):
    #dotted_chart = pm4py.visualization.dotted_chart.factory.apply(event_log)
    #pm4py.visualization.dotted_chart.factory.view(dotted_chart)
    #pm4py.view_dotted_chart(event_log, format='png')

    fig, ax = plt.subplots(figsize=(15, 8))
    sns.scatterplot(data=event_log,
                    x='Time From Start',
                    y='Case ID',
                    hue='Activity',
                    palette="Set1",
                    s=200,
                    ax=ax)
    fig.suptitle('Dotted Chart', fontsize=14)
    ax.set(xlabel='Time from Trace Start (s)', ylabel='Case ID')
    fig.show()

    fig, ax = plt.subplots(figsize=(15, 8))
    sns.scatterplot(data=event_log,
                    x='Time From Start',
                    y='Activity',
                    hue='Case ID',
                    palette="Set1",
                    s=200,
                    ax=ax)
    fig.suptitle('Dotted Chart', fontsize=14)
    ax.set(xlabel='Time from Trace Start (s)', ylabel='Activity')
    fig.show()


def compute_time_from_start(df, datetime_column='Timestamp', case_id_col='Case ID'):
    df = df.sort_values(by=[case_id_col, datetime_column])
    df['Time From Start'] = df.groupby(case_id_col)[datetime_column].transform(lambda x: x - x.min())
    print(df[['Case ID', 'Activity', 'Timestamp', 'Time From Start']])
    return df



def main():
    # read CSV file
    csv_file_path = './running-example.csv'
    df = read_csv(csv_file_path, delimiter=';', datetime_column='Timestamp', datetime_format='%d-%m-%Y:%H.%M')
    # convert to event log
    event_log = convert_to_event_log(df, case_id_col='Case ID', activity_col='Activity', timestamp_col='Timestamp')


    # analyze event log
    analyze_event_log(event_log)

    # compute time from start for each event
    df = compute_time_from_start(df, datetime_column='Timestamp', case_id_col='Case ID')
    # show dotted chart
    show_dotted_chart(df)

    # export to XES file
    output_xes_path = './output.xes'
    #export_event_log(event_log, output_xes_path, format='xes')

if __name__ == '__main__':
    main()