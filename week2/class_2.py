class Animal:
    def __init__(self, nm):
        self.nm = nm

    def speak(self):
        pass

    def move(self):
        print('move move!')

class Dog(Animal):
    def __init__(self, nm, bread):
        super().__init__(nm) # 부모생성자
        self.bread = bread #자식속성

    def speak(self ): #오버라이딩
        print('bark ~ bark!!') #부모의 기능을 다시 정의
class Duck(Animal):
    def speak(self):
        print('quack! quack~!')
dog1 = Dog('라이코스', '닥스훈트')
dog2 = Dog('바미', '보더콜리')
duck1 = Duck('도날드')
print(f'{dog1.nm}은 {dog1.bread}')
dog1.speak() #상속받아 동일한 기능이 있지만  다른 처리
duck1.speak()
duck1.move()
dog2.move() #동일한 기능 수행
