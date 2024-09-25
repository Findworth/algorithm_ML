
import pandas as pd
from typing import List
from functools import reduce
from numpy import pi, sqrt, exp
xigua_data = pd.read_excel(r"C:\Users\LENOVO\Desktop\西瓜.xlsx")
good_mean_density = xigua_data["密度"].loc[xigua_data["好瓜"] == "是"].mean()
bad_mean_density = xigua_data["密度"].loc[xigua_data["好瓜"] == "否"].mean()
good_mean_sugar = xigua_data["含糖率"].loc[xigua_data["好瓜"] == "是"].mean()
bad_mean_sugar = xigua_data["含糖率"].loc[xigua_data["好瓜"] == "否"].mean()
good_var_density = xigua_data["密度"].loc[xigua_data["好瓜"] == "是"].var()
bad_var_density = xigua_data["密度"].loc[xigua_data["好瓜"] == "否"].var()
good_var_sugar = xigua_data["含糖率"].loc[xigua_data["好瓜"] == "是"].var()
bad_var_sugar = xigua_data["含糖率"].loc[xigua_data["好瓜"] == "否"].var()
xigua_data["密度"] = xigua_data["密度"].astype(str)
xigua_data["含糖率"] = xigua_data["含糖率"].astype(str)
all_xigua = len(list(xigua_data.index))
all_class = xigua_data["好瓜"].value_counts()
good = all_class["是"]
bad = all_class["否"]
N = len(all_class)


def calu_discret_prob(attr: str, value: str, xigua_type: str):
    n_modify = len(xigua_data[attr].value_counts())
    if xigua_type == "好瓜":
        xigua_num = good
        value_num = len(xigua_data[(xigua_data[attr] == value) & (xigua_data["好瓜"] == "是")])
        return (value_num + 1) / (xigua_num + n_modify)
    else:
        xigua_num = bad
        value_num = len(xigua_data[(xigua_data[attr] == value) & (xigua_data["好瓜"] == "否")])
        return (value_num + 1) / (xigua_num + n_modify)


def calu_continuous_prob(con_attr: str, con_value: str, xigua_type: str):
    con_value = float(con_value)
    if con_attr == "含糖率" and xigua_type == "好瓜":
        return exp(-(con_value - good_mean_sugar)**2 / (2 * good_var_sugar)) / (sqrt(2*pi) * sqrt(good_var_sugar))
    elif con_attr == "含糖率" and xigua_type == "坏瓜":
        return exp(-(con_value - bad_mean_sugar) ** 2 / (2 * bad_var_sugar)) / (sqrt(2 * pi) * sqrt(bad_var_sugar))
    elif con_attr == "密度" and xigua_type == "好瓜":
        return exp(-(con_value - good_mean_density) ** 2 / (2 * good_var_density)) / (
                    sqrt(2 * pi) * sqrt(good_var_density))
    elif con_attr == "密度" and xigua_type == "坏瓜":
        return exp(-(con_value - bad_mean_density) ** 2 / (2 * bad_var_density)) / (
                    sqrt(2 * pi) * sqrt(bad_var_density))


def judge(dis_attribute: List[str], dis_attr_value: List[str], con_attr: List[str], con_attr_value: List[str]):
    p_pre_good = (good + 1) / (all_xigua + N)
    p_pre_bad = (bad + 1) / (all_xigua + N)

    print(f"修正后好瓜的先验概率为{(good + 1) / (all_xigua + N)}")
    print(f"修正后坏瓜的先验概率为{(bad + 1) / (all_xigua + N)}")
    good_prob_list = []
    bad_prob_list = []
    for i in zip(dis_attribute, dis_attr_value):
        attr = i[0]
        attr_value = i[1]
        good_prob = calu_discret_prob(attr, attr_value, "好瓜")
        bad_prob = calu_discret_prob(attr, attr_value, "坏瓜")
        good_prob_list.append(good_prob)
        bad_prob_list.append(bad_prob)
    for i in zip(con_attr, con_attr_value):
        attr = i[0]
        attr_value = i[1]
        good_prob = calu_continuous_prob(attr, attr_value, "好瓜")
        bad_prob = calu_continuous_prob(attr, attr_value, "坏瓜")
        good_prob_list.append(good_prob)
        bad_prob_list.append(bad_prob)

    good_result = reduce(lambda x, y: x * y, good_prob_list, p_pre_good)
    bad_result = reduce(lambda x, y: x * y, bad_prob_list, p_pre_bad)
    if good_result > bad_result:
        print(f"是好瓜,且概率为{good_result},是坏瓜的概率为{bad_result}")
    else:
        print(f"是坏瓜,且概率为{bad_result}, 是好瓜的概率为{good_result}")


def main():
    print(f"总的西瓜数量是{all_xigua}")
    print(f"好瓜的数量是{good}")
    print(f"坏瓜的数量是{bad}")
    print(f"总共的类别有{len(all_class)}种")
    xigua_dis_attr = input("输入西瓜的离散属性，用空格分隔 ").split()
    dis_attr_value = input("输入每个离散属性的取值，用空格分隔 ").split()
    xigua_con_attr = input("输入西瓜的连续属性，用空格分隔").split()
    con_attr_value = input("输入每个连续属性的取值，用空格分隔 ").split()
    judge(xigua_dis_attr, dis_attr_value, xigua_con_attr, con_attr_value)


if __name__ == "__main__":
    main()
# 示例输入：
# 色泽 根蒂 敲声 纹理 脐部 触感
# 青绿 蜷缩 浊响 清晰 凹陷 硬滑
# 密度 含糖率
# 0.697 0.460
