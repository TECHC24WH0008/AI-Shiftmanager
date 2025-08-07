import tkinter as tk
from tkinter import ttk, filedialog
from version import __version__
import pandas as pd

class Staff:
    def __init__(self, name, preferred_days, available_times, max_days, role, ability):
        self.name = name
        self.preferred_days = preferred_days
        self.available_times = available_times
        self.max_days = max_days
        self.role = role
        self.ability = ability
        self.assigned_days = 0
        self.assigned_slots = []

class ShiftApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"シフト自動割当 v{__version__}")
        self.staffs = []

        # スタッフ情報入力欄
        self.staff_frame = tk.LabelFrame(root, text="スタッフ情報")
        self.staff_frame.pack(fill="x", padx=5, pady=5)
        self.name_var = tk.StringVar()
        tk.Label(self.staff_frame, text="名前").grid(row=0, column=0)
        tk.Entry(self.staff_frame, textvariable=self.name_var, width=8).grid(row=0, column=1)
        self.days_var = tk.StringVar()
        tk.Label(self.staff_frame, text="希望日(例:1,2,3)").grid(row=0, column=2)
        tk.Entry(self.staff_frame, textvariable=self.days_var, width=10).grid(row=0, column=3)
        self.times_var = tk.StringVar()
        tk.Label(self.staff_frame, text="時間(例:8,9,10)").grid(row=0, column=4)
        tk.Entry(self.staff_frame, textvariable=self.times_var, width=10).grid(row=0, column=5)
        self.maxdays_var = tk.IntVar(value=5)
        tk.Label(self.staff_frame, text="最大日数").grid(row=0, column=6)
        tk.Entry(self.staff_frame, textvariable=self.maxdays_var, width=3).grid(row=0, column=7)
        self.role_var = tk.StringVar(value="一般")
        tk.Label(self.staff_frame, text="役割").grid(row=0, column=8)
        ttk.Combobox(self.staff_frame, textvariable=self.role_var, values=["一般", "責任者"], width=6).grid(row=0, column=9)
        self.ability_var = tk.IntVar(value=1)
        tk.Label(self.staff_frame, text="能力値").grid(row=0, column=10)
        tk.Entry(self.staff_frame, textvariable=self.ability_var, width=3).grid(row=0, column=11)
        tk.Button(self.staff_frame, text="追加", command=self.add_staff).grid(row=0, column=12)

        self.staff_listbox = tk.Listbox(self.staff_frame, width=90)
        self.staff_listbox.grid(row=1, column=0, columnspan=13, pady=3)

        # Excel読込ボタン
        tk.Button(root, text="Excelからスタッフ読込", command=self.load_staffs_excel).pack(pady=3)

        # --- 全体設定 ---
        global_frame = tk.LabelFrame(root, text="全体設定")
        global_frame.pack(fill="x", padx=5, pady=5)

        # 休みの日
        self.global_holidays_var = tk.StringVar(value="6,7")
        tk.Label(global_frame, text="休みの日（曜日番号カンマ区切り、例:6,7）").grid(row=0, column=0)
        tk.Entry(global_frame, textvariable=self.global_holidays_var, width=10).grid(row=0, column=1)
        # 始業・就業時間
        self.global_start_time_var = tk.IntVar(value=8)
        tk.Label(global_frame, text="始業時間").grid(row=0, column=2)
        tk.Entry(global_frame, textvariable=self.global_start_time_var, width=3).grid(row=0, column=3)
        self.global_end_time_var = tk.IntVar(value=18)
        tk.Label(global_frame, text="就業時間").grid(row=0, column=4)
        tk.Entry(global_frame, textvariable=self.global_end_time_var, width=3).grid(row=0, column=5)

        # 必要能力値欄
        self.num_frame = tk.LabelFrame(root, text="時間帯ごとの必要人数・能力値 (曜日×時間)")
        self.num_frame.pack(fill="x", padx=5, pady=5)
        self.hour_num_vars = {}
        self.min_ability_vars = {}
        self.days = [1,2,3,4,5,6,7]
        self.hours = list(range(8,21))
        daynames = ["月", "火", "水", "木", "金", "土", "日"]
        for i, day in enumerate(self.days):
            tk.Label(self.num_frame, text=daynames[i]).grid(row=i+1, column=0)
            self.hour_num_vars[day] = {}
            for j, hour in enumerate(self.hours):
                var = tk.IntVar(value=3)
                self.hour_num_vars[day][hour] = var
                tk.Entry(self.num_frame, textvariable=var, width=2).grid(row=i+1, column=j+1)
                if i == 0:
                    tk.Label(self.num_frame, text=f"{hour}時").grid(row=0, column=j+1)
        # 能力値欄
        tk.Label(self.num_frame, text="必要能力値合計").grid(row=8, column=0)
        for j, hour in enumerate(self.hours):
            var = tk.IntVar(value=5)
            self.min_ability_vars[hour] = var
            tk.Entry(self.num_frame, textvariable=var, width=2).grid(row=8, column=j+1)

        # 1日最大・最小勤務時間
        self.max_work_var = tk.IntVar(value=8)
        self.min_work_var = tk.IntVar(value=4)
        tk.Label(root, text="1日最大勤務時間").pack()
        tk.Entry(root, textvariable=self.max_work_var, width=3).pack()
        tk.Label(root, text="1日最小勤務時間").pack()
        tk.Entry(root, textvariable=self.min_work_var, width=3).pack()

        # 各時間帯の責任者必要数
        self.leader_var = tk.IntVar(value=1)
        tk.Label(root, text="各時間帯の責任者必要数").pack()
        tk.Entry(root, textvariable=self.leader_var, width=3).pack()

        # シフト生成ボタン
        tk.Button(root, text="シフト生成", command=self.generate_shift).pack(pady=5)

        # 結果表示欄
        self.result_frame = tk.LabelFrame(root, text="割当結果")
        self.result_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.result_text = tk.Text(self.result_frame, height=20)
        self.result_text.pack(fill="both", expand=True)

        # バージョン表示
        tk.Label(root, text=f"バージョン: {__version__}").pack(side="bottom")

    def add_staff(self):
        name = self.name_var.get()
        days = [int(x) for x in self.days_var.get().split(",") if x.strip().isdigit()]
        times = [int(x) for x in self.times_var.get().split(",") if x.strip().isdigit()]
        max_days = self.maxdays_var.get()
        role = self.role_var.get()
        ability = self.ability_var.get()
        staff = Staff(name, days, times, max_days, role, ability)
        self.staffs.append(staff)
        self.staff_listbox.insert(
            tk.END,
            f"{name} / 希望日:{days} / 時間:{times} / 最大:{max_days} / {role} / 能力:{ability}"
        )

    def load_staffs_excel(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if not file_path:
            return
        df = pd.read_excel(file_path)
        self.staffs = []
        self.staff_listbox.delete(0, tk.END)
        for _, row in df.iterrows():
            name = str(row.get("名前", ""))
            preferred_days = [int(x) for x in str(row.get("希望日", "")).split(",") if x.strip().isdigit()]
            available_times = [int(x) for x in str(row.get("希望時間", "")).split(",") if x.strip().isdigit()]
            max_days = int(row.get("最大日数", 0))
            role = str(row.get("役割", "一般"))
            ability = int(row.get("能力値", 1))
            staff = Staff(name, preferred_days, available_times, max_days, role, ability)
            self.staffs.append(staff)
            self.staff_listbox.insert(
                tk.END,
                f"{staff.name} / 希望日:{staff.preferred_days} / 時間:{staff.available_times} / 最大:{staff.max_days} / {staff.role} / 能力:{staff.ability}"
            )

    def generate_shift(self):
        need_nums = {}
        for day in self.days:
            need_nums[day] = {}
            for hour in self.hours:
                need_nums[day][hour] = self.hour_num_vars[day][hour].get()
        min_ability_per_hour = {hour: self.min_ability_vars[hour].get() for hour in self.hours}
        config = {
            "DAYS": self.days,
            "HOURS": self.hours,
            "NEED_NUMS_PER_HOUR": need_nums,
            "LEADER_NEEDED": self.leader_var.get(),
            "min_ability_per_hour": min_ability_per_hour,
            "max_work_time": self.max_work_var.get(),
            "min_work_time": self.min_work_var.get(),
            "global_holidays": [int(x) for x in self.global_holidays_var.get().split(",") if x.strip().isdigit()],
            "global_start_time": self.global_start_time_var.get(),
            "global_end_time": self.global_end_time_var.get()
        }
        from scheduler import assign_shifts
        slots = assign_shifts(self.staffs, config)
        self.result_text.delete(1.0, tk.END)
        daynames = ["月", "火", "水", "木", "金", "土", "日"]
        for slot in slots:
            day_idx = slot["day"] - 1
            day_label = daynames[day_idx] if 0 <= day_idx < 7 else str(slot["day"])
            hour = slot["hour"]
            assigned = ",".join(slot["assigned"])
            self.result_text.insert(tk.END, f"{day_label}曜 {hour}時: {assigned}\n")

def main():
    root = tk.Tk()
    app = ShiftApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()