import tkinter as tk
from tkinter import ttk
import threading
import time
import random
# PIL 사용 시 주석 해제 (필요에 따라 사용)
# from PIL import Image, ImageTk

class LearningDataCreationUI:
    def __init__(self, root):
        self.root = root
        self.root.title("학습데이터 생성 메뉴")

        # 시뮬레이션 관련 변수 초기화
        self.simulation_running = False
        self.sim_time = 0  # 시뮬레이션 시간(분 단위)
        self.sim_speed = 1  # 시뮬레이션 배속 (1x, 2x, 3x, 5x, 10x)

        # 각 디바이스(방)의 기본 색상 및 활성화 색상 설정
        self.off_colors = {"거실": "lightblue", "주방": "lightgreen", "침실": "lightyellow", "욕실": "lightpink"}
        self.on_colors = {"거실": "blue", "주방": "green", "침실": "gold", "욕실": "red"}

        # 평면도 상의 방 사각형 id를 저장할 딕셔너리
        self.room_rects = {}

        # 전체 화면을 상단 Frame(제목영역) / 메인영역(좌측=평면도, 우측=시계+테이블)으로 구분
        self.top_frame = tk.Frame(self.root, height=50, bg="lightgray")
        self.top_frame.pack(side=tk.TOP, fill=tk.X)
        
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # 상단: 제목 표시
        self.title_label = tk.Label(self.top_frame, text="학습데이터 생성", font=("Helvetica", 16, "bold"), bg="lightgray")
        self.title_label.pack(padx=10, pady=10, anchor="w")
        
        # 메인영역: 좌우 2분할 (왼쪽=평면도, 오른쪽=시계+표)
        self.left_frame = tk.Frame(self.main_frame, width=400, height=500, bg="white")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.right_frame = tk.Frame(self.main_frame, width=400, height=500)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 좌측 프레임에 평면도 그리기 (Canvas 사용)
        self.floorplan_canvas = tk.Canvas(self.left_frame, width=380, height=480, bg="white")
        self.floorplan_canvas.pack(padx=10, pady=10)
        self.draw_floorplan()
        
        # 우측 프레임을 상단(시계/달력 및 시뮬레이션 시간) / 하단(테이블 입력영역)으로 구분
        self.right_top_frame = tk.Frame(self.right_frame, height=200, bg="white")
        self.right_top_frame.pack(side=tk.TOP, fill=tk.X)
        self.right_bottom_frame = tk.Frame(self.right_frame)
        self.right_bottom_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # (오른쪽 상단) 시계/달력 인터페이스 부분: 간단히 Label로 대체
        clock_label = tk.Label(self.right_top_frame, text="시계/달력 인터페이스 (예시)", font=("Helvetica", 12), bg="white")
        clock_label.pack(padx=5, pady=5, anchor="center")

        # 시뮬레이션 시간 표시 레이블 추가
        self.sim_time_label = tk.Label(self.right_top_frame, text="시뮬레이션 시간: 00:00", font=("Helvetica", 12), bg="white")
        self.sim_time_label.pack(padx=5, pady=5, anchor="center")
        
        # (오른쪽 하단) 테이블(Grid 또는 Treeview)을 이용한 학습데이터 입력
        table_label = tk.Label(self.right_bottom_frame, text="학습데이터 입력 (From / To / Activity 등)", font=("Helvetica", 12, "bold"))
        table_label.pack(padx=5, pady=5, anchor="w")
        
        # Treeview 예시
        columns = ("device", "from", "to", "activity")
        self.tree = ttk.Treeview(self.right_bottom_frame, columns=columns, show="headings", height=5)
        self.tree.heading("device", text="Device(#)")
        self.tree.heading("from", text="From")
        self.tree.heading("to", text="To")
        self.tree.heading("activity", text="Activity")
        
        self.tree.column("device", width=80, anchor="center")
        self.tree.column("from", width=80, anchor="center")
        self.tree.column("to", width=80, anchor="center")
        self.tree.column("activity", width=120, anchor="center")
        self.tree.pack(padx=5, pady=5, fill=tk.X)
        
        # 샘플 데이터(디바이스 #1~5) 추가
        sample_data = [
            ("#1", "17:30", "20:00", "조명 OFF"),
            ("#2", "20:00", "22:00", "보일러 ON"),
            ("#3", "22:00", "23:00", "가스밸브 확인"),
            ("#4", "23:00", "07:00", "취침모드"),
            ("#5", "07:00", "08:00", "조명 ON")
        ]
        for row in sample_data:
            self.tree.insert("", tk.END, values=row)
        
        # 버튼 프레임: 기존 버튼과 시뮬레이션 제어, 배속 설정 버튼 추가
        button_frame = tk.Frame(self.right_bottom_frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        gen_button = tk.Button(button_frame, text="유사 생활패턴 생성 (Week day)", command=self.generate_pattern)
        gen_button.pack(side=tk.LEFT, padx=5)
        detail_button = tk.Button(button_frame, text="상세설정기반 생성", command=self.detail_settings)
        detail_button.pack(side=tk.LEFT, padx=5)
        
        sim_start_button = tk.Button(button_frame, text="시뮬레이션 시작", command=self.start_simulation)
        sim_start_button.pack(side=tk.LEFT, padx=5)
        sim_stop_button = tk.Button(button_frame, text="시뮬레이션 중지", command=self.stop_simulation)
        sim_stop_button.pack(side=tk.LEFT, padx=5)
        
        # 배속 설정 UI: 배속 레이블과 콤보박스 추가
        speed_label = tk.Label(button_frame, text="배속:", font=("Helvetica", 12))
        speed_label.pack(side=tk.LEFT, padx=(20, 5))
        self.speed_combobox = ttk.Combobox(button_frame, values=["1", "2", "3", "5", "10"], width=3, state="readonly")
        self.speed_combobox.set("1")
        self.speed_combobox.pack(side=tk.LEFT)
        self.speed_combobox.bind("<<ComboboxSelected>>", self.on_speed_change)
    
    def draw_floorplan(self):
        # 평면도 캔버스에 각 방을 사각형과 텍스트로 표시
        # 거실 (좌측 상단): (10,10) ~ (190,150)
        rect_id = self.floorplan_canvas.create_rectangle(10, 10, 190, 150, fill=self.off_colors["거실"], outline="black", width=2)
        self.room_rects["거실"] = rect_id
        self.floorplan_canvas.create_text(100, 80, text="거실", font=("Helvetica", 14, "bold"))
        
        # 주방 (우측 상단): (200,10) ~ (370,100)
        rect_id = self.floorplan_canvas.create_rectangle(200, 10, 370, 100, fill=self.off_colors["주방"], outline="black", width=2)
        self.room_rects["주방"] = rect_id
        self.floorplan_canvas.create_text(285, 55, text="주방", font=("Helvetica", 14, "bold"))
        
        # 침실 (좌측 하단): (10,160) ~ (190,280)
        rect_id = self.floorplan_canvas.create_rectangle(10, 160, 190, 280, fill=self.off_colors["침실"], outline="black", width=2)
        self.room_rects["침실"] = rect_id
        self.floorplan_canvas.create_text(100, 220, text="침실", font=("Helvetica", 14, "bold"))
        
        # 욕실 (우측 하단): (200,110) ~ (370,280)
        rect_id = self.floorplan_canvas.create_rectangle(200, 110, 370, 280, fill=self.off_colors["욕실"], outline="black", width=2)
        self.room_rects["욕실"] = rect_id
        self.floorplan_canvas.create_text(285, 195, text="욕실", font=("Helvetica", 14, "bold"))
    
    def generate_pattern(self):
        # 유사 생활패턴 생성 로직 (추가 구현)
        print("유사 생활패턴 생성 로직 실행")
    
    def detail_settings(self):
        # 상세설정기반 생성 로직 (추가 구현)
        print("상세설정기반 생성 로직 실행")
    
    def on_speed_change(self, event):
        # 콤보박스에서 선택된 배속 값으로 시뮬레이션 배속을 업데이트
        selected = self.speed_combobox.get()
        try:
            self.sim_speed = float(selected)
            print(f"시뮬레이션 배속 {self.sim_speed}배로 설정됨")
        except ValueError:
            self.sim_speed = 1

    def start_simulation(self):
        if not self.simulation_running:
            self.simulation_running = True
            self.sim_time = 0
            self.simulation_thread = threading.Thread(target=self.simulation_loop)
            self.simulation_thread.daemon = True
            self.simulation_thread.start()
            print("시뮬레이션 시작")
            
    def stop_simulation(self):
        if self.simulation_running:
            self.simulation_running = False
            print("시뮬레이션 중지")
            
    def simulation_loop(self):
        # 시뮬레이션 루프: 1초마다 시뮬레이션 시간(분)을 sim_speed만큼 증가시키고 임의 이벤트 생성
        while self.simulation_running:
            time.sleep(1)  # 1초마다 업데이트
            self.sim_time += self.sim_speed  # 배속에 따라 시간 증가
            # 시뮬레이션 시간 업데이트 (HH:MM 형식)
            hours = (int(self.sim_time) // 60) % 24
            minutes = int(self.sim_time) % 60
            sim_time_str = f"{hours:02d}:{minutes:02d}"
            self.root.after(0, lambda t=sim_time_str: self.sim_time_label.config(text=f"시뮬레이션 시간: {t}"))
            
            # 임의 이벤트 생성: 50% 확률로 이벤트 발생
            if random.random() < 0.5:
                # 임의 디바이스 선택
                device = random.choice(["거실", "주방", "침실", "욕실"])
                # 이벤트 시간: 현재 시뮬레이션 시간
                event_time = sim_time_str
                # 이벤트 액티비티: ON 또는 OFF 중 임의 선택
                activity = random.choice(["ON", "OFF"])
                # Treeview에 새 이벤트 데이터 추가 (이벤트 발생 시간을 'from'에 기록하고, 'to'는 '-' 처리)
                self.root.after(0, lambda d=device, t=event_time, act=activity: self.tree.insert("", tk.END, values=(d, t, "-", act)))

                # 해당 디바이스의 평면도 사각형 색상 업데이트
                if device in self.room_rects:
                    if activity == "ON":
                        new_color = self.on_colors[device]
                    else:
                        new_color = self.off_colors[device]
                    self.root.after(0, lambda d=device, color=new_color: self.floorplan_canvas.itemconfig(self.room_rects[d], fill=color))

if __name__ == "__main__":
    root = tk.Tk()
    app = LearningDataCreationUI(root)
    root.mainloop()