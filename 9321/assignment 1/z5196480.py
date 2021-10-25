import pandas as pd
import matplotlib.pyplot as plt


def question_1():
    df1 = pd.read_csv('Olympics_dataset1.csv', skiprows=1, thousands=',')
    df1_1 = pd.read_csv('Olympics_dataset2.csv', skiprows=1, thousands=',')
    df1_2 = df1_1.drop(df1_1.columns[5:-1], axis=1)
    df1.columns = ['Country', 'summer_rubbish', 'summer_participation', 'summer_gold', 'summer_silver', 'summer_bronze',
                   'summer_total']
    df1_2.columns = ['Country', 'winter_participation', 'winter_gold', 'winter_silver', 'winter_bronze',
                     'winter_total']
    df1_f = pd.merge(df1, df1_2, on='Country')
    df1_f = df1_f.drop(df1_f.tail(1).index)  # this is ok
    return df1_f



def question_2():
    df2 = question_1()
    df2['Country'] = df2['Country'].str.split('(',expand=True)[0]
    df2['Country'] = df2['Country'].str.strip(' ')
    df2.set_index(['Country'], inplace=True)
    df2 = df2.drop(columns=['summer_rubbish', 'summer_total', 'winter_total'])
    return df2


def question_3():
    df3 = question_2()
    df3 = df3.dropna(axis=0,how='any')
    return df3


def question_4():
    df4 = question_3()
    max_summer_gold = df4[df4['summer_gold'] == df4['summer_gold'].max()]
    print(max_summer_gold.index[0])


def question_5():
    df5 = question_3()
    max_differce_gold = df5[
        abs(df5['summer_gold'] - df5['winter_gold']) == abs(df5['summer_gold'] - df5['winter_gold']).max()]
    max_differce_gold['num'] = abs(max_differce_gold.summer_gold - max_differce_gold.winter_gold)
    print(max_differce_gold.index[0],max_differce_gold.loc[max_differce_gold.index[0],'num'])


def question_6():
    df_6 = question_3()
    df_6['sum_medals'] = df_6['summer_gold'] + df_6['summer_silver'] + df_6['summer_bronze'] + df_6['winter_gold'] + df_6['winter_silver'] + df_6['winter_bronze']
    df_6.sort_values('sum_medals', ascending=False, inplace=True)
    return df_6


def question_7():
    df_7 = question_6().head(10)
    df_7['summer_madals'] = df_7['summer_gold'] + df_7['summer_silver'] + df_7['summer_bronze']
    df_7['winter_madals'] = df_7['winter_gold'] + df_7['winter_silver'] + df_7['winter_bronze']
    df_7plot = pd.DataFrame({'winter_madals': df_7['winter_madals'], 'summer_madals': df_7['summer_madals']})
    df_7plot.plot(kind='barh', figsize=(12, 8), legend=True, fontsize=12, stacked=True, grid=True,
                  title="Medals for Winter and Summer Games").legend(loc='lower center', bbox_to_anchor=(0.5, -0.15),
                                                                     ncol=2, frameon=False)
    plt.show()

def question_8():
    df_8 = question_3()
    df_8 = df_8.loc[['United States', 'Australia', 'Great Britain', 'Japan', 'New Zealand']]
    df_8plot = pd.DataFrame({'winter_gold': df_8['winter_gold'], 'winter_silver': df_8['winter_silver'],
                             'winter_bronze': df_8['winter_bronze']})
    df_8plot.plot(kind='bar', figsize=(12, 8), legend=True, fontsize=12, stacked=False, rot=0, grid=True,
                  title="Winter Games").legend(loc='lower center', bbox_to_anchor=(0.5, -0.15), ncol=3, frameon=False)
    plt.show()

def question_9():
    df_9 = question_3()
    df_9['summer_rate'] = df_9.apply(
        lambda x: (x['summer_gold'] * 5 + x['summer_silver'] * 3 + x['summer_bronze']) / x['summer_participation'] if x[
                                                                                                                          'summer_participation'] != 0 else 0,
        axis=1)
    df_9.sort_values('summer_rate', ascending=False, inplace=True)
    df_9q = df_9.head(5)
    for index, row in df_9q.iterrows():
        print(f'{index:20}\t{row[-1]:5.2f}')


def question_10():
    df_10 = question_3()
    df_10['summer_rate'] = df_10.apply(
        lambda x: (x['summer_gold'] * 5 + x['summer_silver'] * 3 + x['summer_bronze']) / x['summer_participation'] if x[
                                                                                                                          'summer_participation'] != 0 else 0,
        axis=1)
    df_10.sort_values('summer_rate', ascending=False, inplace=True)
    df_10['winter_rate'] = df_10.apply(
        lambda x: (x['winter_gold'] * 5 + x['winter_silver'] * 3 + x['winter_bronze']) / x['winter_participation'] if x[
                                                                                                                          'winter_participation'] != 0 else 0,
        axis=1)
    df_color = pd.read_csv('Countries-Continents.csv')
    df_10_color = pd.merge(df_10, df_color, how='left', on='Country')
    df_10_color.plot(x='summer_rate', y='winter_rate', kind='scatter', figsize=(20, 8), grid=True)
    for (index, rows) in df_10_color.iterrows():
        plt.text((rows['summer_rate'] - 13), (rows['winter_rate'] + 1), rows['Country'], ha='left', va='bottom')
    plt.ylabel('Winter_Rate')
    plt.xlabel('Summer_Rate')
    plt.show()
    '''
    colors = {'1': ['Africa', 'black'], '2': ['Europe', 'blue'], '3': ['North America', 'red'],
              '4': ['South America', 'orange'], '5': ['Asia', 'yellow'], '6': ['Oceania', 'green'],
              '7': ['NaN', 'grey']}
    pd_c = pd.DataFrame.from_dict(colors, orient='index', columns=['Continent', 'color'])
    # pd_c.set_index(['Continent'], inplace=True)
    df_10_color = pd.merge(df_10_color, pd_c)
    ax = df_10_color.plot(x='summer_rate', y='winter_rate', kind='scatter', figsize=(20, 8), grid=True)
    for (index, rows) in df_10_color.iterrows():
        df_10_color.plot(ax=ax,x='summer_rate', y='winter_rate', kind='scatter', figsize=(20, 8), grid=True, color=rows['color'])
        plt.text((rows['summer_rate'] - 10), (rows['winter_rate'] + 1), rows['Country'], ha='left', va='bottom')
    plt.ylabel('Winter_Rate')
    plt.xlabel('Summer_Rate')
    plt.show()    ???? 
    '''








if __name__ == "__main__":
    print("--------------- question_1 ---------------")
    print(question_1().head(5).to_string())
    print()
    print("--------------- question_2 ---------------")
    print(question_2().head(5).to_string())
    print()
    print("--------------- question_3 ---------------")
    print(question_3().tail(10).to_string())
    print()
    print("--------------- question_4 ---------------")
    question_4()
    print()
    print("--------------- question_5 ---------------")
    question_5()
    print()
    print("--------------- question_6 ---------------")
    print(question_6().head(1).append(question_6().tail(5)).to_string())
    print()
    print("--------------- question_7 ---------------")
    question_7()
    print()
    print("--------------- question_8 ---------------")
    question_8()
    print()
    print("--------------- question_9 ---------------")
    question_9()
    print()
    print("--------------- question_10 ---------------")
    question_10()