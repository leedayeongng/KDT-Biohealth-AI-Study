class CoffeFranchise:
    branch=0 #클래스 변수
    def __init__(self, nm, beans=None, menu=None):
        self.nm = nm #인스턴수 변수(각인스턴스는 다른값을 가지게 된다)
        self.beans = beans
        self.menu = menu
        self.new_branch() #클래스변수증가
    @classmethod  # 클래스매소드
    def now_branch_cnt(cls):
         print(f'현재 {cls.branch}개의 지점이 있습니다.')
    @classmethod
    def new_branch(cls): #cls : 해cl당클래스만 접근할수있는변수
        cls.branch += 1

    def make_coffe(self): #인스턴스 메서드
        if self.beans:
            print(f"{self.nm}에서는 {self.beans}으로 커피를 만들어요^^")
        else:
            print(f"{self.nm}에서는 신선한 커피를 제공합니다.")
    @staticmethod
    def fn_print():
        print('정적 메소드')

future = CoffeFranchise("미래융합점","미래 브랜드","아아")
city = CoffeFranchise("둔산점")
print(f'인스턴스 1: {future.nm},인스턴스 2:{city.nm}')
CoffeFranchise.now_branch_cnt()

future.make_coffe()
city.make_coffe()
CoffeFranchise.fn_print() #정적메소드

class test():
    def fn_test(self):
        print('hi')
t = test()
t.fn_test()