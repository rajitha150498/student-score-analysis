import pandas as pd
import matplotlib.pyplot as plt
import os

# ── LOAD DATA ──
df = pd.read_csv('students.csv')
print("✅ Data loaded successfully!")
print(f"Total students: {len(df)}")
print()

# ── CLEAN DATA ──
df = df.dropna()
print("✅ Data cleaned!")
print()

# ── BASIC STATS ──
subjects = ['Math', 'Science', 'English', 'History', 'Computer']
df['Average'] = df[subjects].mean(axis=1).round(2)
df['Grade'] = df['Average'].apply(lambda x: 
    'A' if x >= 90 else 'B' if x >= 80 else 'C' if x >= 70 else 'D' if x >= 60 else 'F')

print("📊 STUDENT PERFORMANCE SUMMARY")
print("="*40)
print(f"Highest Average: {df['Average'].max()} — {df.loc[df['Average'].idxmax(), 'Name']}")
print(f"Lowest Average:  {df['Average'].min()} — {df.loc[df['Average'].idxmin(), 'Name']}")
print(f"Class Average:   {df['Average'].mean().round(2)}")
print()
print("📈 Subject Averages:")
for s in subjects:
    print(f"  {s}: {df[s].mean().round(2)}")
print()
print("🎓 Grade Distribution:")
print(df['Grade'].value_counts().to_string())
print()

# ── CHARTS ──
os.makedirs('charts', exist_ok=True)
plt.style.use('seaborn-v0_8-darkgrid')

# Chart 1 — Subject averages bar chart
fig, ax = plt.subplots(figsize=(10, 6))
colors = ['#4e79a7','#f28e2b','#e15759','#76b7b2','#59a14f']
bars = ax.bar(subjects, [df[s].mean() for s in subjects], color=colors, width=0.5)
ax.set_title('Average Score by Subject', fontsize=16, fontweight='bold', pad=15)
ax.set_ylabel('Average Score', fontsize=12)
ax.set_ylim(0, 100)
for bar, val in zip(bars, [df[s].mean() for s in subjects]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
            f'{val:.1f}', ha='center', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig('charts/subject_averages.png', dpi=150)
plt.close()
print("✅ Chart 1 saved: subject_averages.png")

# Chart 2 — Grade distribution pie chart
fig, ax = plt.subplots(figsize=(8, 8))
grade_counts = df['Grade'].value_counts()
colors_pie = ['#59a14f','#4e79a7','#f28e2b','#e15759','#b07aa1']
wedges, texts, autotexts = ax.pie(grade_counts.values, labels=grade_counts.index,
    autopct='%1.1f%%', colors=colors_pie[:len(grade_counts)],
    startangle=90, pctdistance=0.85)
for text in autotexts:
    text.set_fontsize(12)
    text.set_fontweight('bold')
ax.set_title('Grade Distribution', fontsize=16, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('charts/grade_distribution.png', dpi=150)
plt.close()
print("✅ Chart 2 saved: grade_distribution.png")

# Chart 3 — Top 5 students bar chart
fig, ax = plt.subplots(figsize=(10, 6))
top5 = df.nlargest(5, 'Average')
bars = ax.barh(top5['Name'], top5['Average'], color='#4e79a7')
ax.set_title('Top 5 Students by Average Score', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Average Score', fontsize=12)
ax.set_xlim(0, 100)
for bar, val in zip(bars, top5['Average']):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
            f'{val}', va='center', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig('charts/top5_students.png', dpi=150)
plt.close()
print("✅ Chart 3 saved: top5_students.png")

print()
print("🎉 Analysis complete! Check the charts folder.")