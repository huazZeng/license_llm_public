import pandas as pd

# 读取CSV文件
df = pd.read_csv('Data\\license\\liresolver\\tldr-licenses-forSpdx.csv')
license_columns = ['license']
df_license = df[license_columns]
# 定义前11列和第12列及之后的列名
right_columns = [
    "Distribute", "Modify", "Commercial Use", "Relicense", "Hold Liable",
    "Use Patent Claims", "Sublicense", "Statically Link", "Private Use",
    "Use Trademark", "Place Warranty"
]

obligation_columns = [
    "Include Copyright", "Include License", "Include Notice", "Disclose Source",
    "State Changes", "Include Original", "Give Credit", "Rename", "Contact Author",
    "Include Install Instructions", "Compensate for Damages", "Pay Above Use Threshold"
]

# 获取前11列的数据
df_right = df[right_columns]

# 获取第12列及其之后的数据
df_obligation= df[obligation_columns]

# 将 "nomentioned" 替换为其他值，例如 "other"
df_right = df_right.replace("NOmentioned", "cannot")
df_obligation = df_obligation.replace("NOmentioned", "can")

# 合并前11列和第12列及其之后的列
df_combined = pd.concat([df_license,df_right, df_obligation], axis=1)
df_rightresult = pd.concat([df_license,df_right], axis=1)
df_obligationresult = pd.concat([df_license,df_obligation], axis=1)
# 保存合并后的数据到新文件
right_file = 'Data\\license\\rightresult.csv'
obligation_file = 'Data\\license\\obligationresult.csv'
output_file = 'Data\\license\\fixedresult.csv'
df_combined.to_csv(output_file, index=False)
df_rightresult.to_csv(right_file,index=False)
df_obligationresult.to_csv(obligation_file,index=False)
print(f"合并后的数据已保存到 {output_file}")


